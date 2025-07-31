from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime
from openai import OpenAI
from fetch_data import search_projects, get_project_details
import sqlite3
import logging
from flask_cors import CORS  # Optional if you're running frontend separately

# Load environment variables
load_dotenv()

# Init conversation history
conversation_history = []

#init openai client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

response = client.responses.create(
    model="gpt-4o-mini",
    instructions="You are an expert in global charities, nonprofit evaluation, and effective giving.",
    input="How do I check if a charity is effective?",
)

print(response.output_text)


def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect("data/altrue.db")


def parse_intent(message):
    """Extract basic cause area and region/keyword from user input."""
    message = message.lower()
    return {
        "theme": "education" if "education" in message else None,
        "keyword": "kenya" if "kenya" in message else None  # update as needed
    }


def generate_response(user_message):
    """
    Parse user message, fetch relevant charity data, and generate a GPT response.
    """
    intent = parse_intent(user_message)
    projects = search_projects(intent.get("theme") or intent.get("keyword"))
    detailed_projects = [get_project_details(p["id"]) for p in projects]

    project_text = "\n\n".join([
        f"{p.get('title')}\n{p.get('summary')}\n{p.get('projectLink')}"
        for p in detailed_projects
    ]) or "No matching projects found."

    messages = [
        {"role": "system", "content": "You are a global charity recommender who suggests high-impact nonprofit projects based on a user's interests and goals."},
        {"role": "user", "content": f"{user_message}\n\nRelevant projects:\n{project_text}"}
    ]

    response = openai.response.create(model="gpt-4o", messages=messages)
    return response.choices[0].message["content"], intent


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
    CORS(app)  # Optional but useful for frontend testing

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.json
            user_message = data.get('message', '')
            selected_model = data.get('model', 'gpt-3.5-turbo')
            prompt_type = data.get('prompt_type', 'direct')

            if not user_message:
                return jsonify({'error': 'No message provided'}), 400

            conn = connect_db()
            cursor = conn.cursor()

            # Parse intent
            gpt_reply, intent = generate_response(user_message)

            # Save user query
            cursor.execute('''
                INSERT INTO queries (user_query, topic, location, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (
                user_message,
                intent.get("theme"),
                intent.get("keyword"),
                datetime.now().isoformat()
            ))
            query_id = cursor.lastrowid

            # Save response
            structured_output = {
                "cause_area": intent.get("theme"),
                "region": intent.get("keyword"),
                "llm_response": gpt_reply
            }

            cursor.execute('''
                INSERT INTO responses (query_id, model_used, projects_json, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (
                query_id,
                selected_model,
                json.dumps(structured_output),
                datetime.now().isoformat()
            ))

            conn.commit()
            conn.close()

            return jsonify({
                "response": structured_output,
                "query_id": query_id,
                "model": selected_model,
                "prompt_type": prompt_type,
                "timestamp": datetime.now().isoformat()
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/history', methods=['GET'])
    def get_history():
        return jsonify({'history': conversation_history})

    @app.route('/api/clear', methods=['POST'])
    def clear_history():
        conversation_history.clear()
        return jsonify({'message': 'History cleared'})

    @app.route('/api/test-globalgiving')
    def test_globalgiving():
        """Test endpoint to validate GlobalGiving API."""
        try:
            base_url = "https://api.globalgiving.org/api/public/projectservice/search/projects"
            params = {
                'q': 'education',
                'api_key': os.getenv("GLOBAL_GIVING_API_KEY"),
                'start': 0
            }
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'AltrueBot/1.0'
            }

            response = requests.get(base_url, params=params, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return jsonify({
                    'status': 'success',
                    'total_projects': len(data.get('projects', {}).get('project', [])),
                    'sample_data': data.get('projects', {}).get('project', [])[0]
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': f'API returned status code: {response.status_code}'
                }), response.status_code

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Error: {str(e)}'
            }), 500

    return app

# ----------- RUN APP -----------

if __name__ == '__main__':
    print("Starting Altrue Chatbot...")
    print("Open your browser to: http://127.0.0.1:5000/")
    logging.basicConfig(level=logging.INFO)
    logging.info("⚡ Flask app starting up...")
    app = create_app()
    app.run(debug=True, use_reloader=False)
