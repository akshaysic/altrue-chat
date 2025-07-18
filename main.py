from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime


# Load environment variables from .env
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

    # Home route - render the chatbot interface
    @app.route('/')
    def home():
        return render_template('index.html')

    # API endpoint to handle chat messages
    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.json
            user_message = data.get('message', '')
            selected_model = data.get('model', 'gpt-3.5-turbo')
            prompt_type = data.get('prompt_type', 'direct')  # support prompt variation

            if not user_message:
                return jsonify({'error': 'No message provided'}), 400

            # Connect to DB
            conn = connect("data/altrue.db")
            cursor = conn.cursor()

            # Save query to DB
            cursor.execute('''
                INSERT INTO queries (user_query)
                VALUES (?)
            ''', (user_message,))
            query_id = cursor.lastrowid

            # Simulate LLM structured response (to replace with OpenAI later)
            structured_output = {
                "cause_area": "education",
                "region": "East Africa",
                "recommended_charities": [
                    {"name": "Books for Africa", "impact_summary": "Provides textbooks and learning materials."},
                    {"name": "Educate!", "impact_summary": "Delivers skills-based education in Uganda."}
                ]
            }

            # Store response in DB
            cursor.execute('''
                INSERT INTO responses (query_id, model_used, projects_json, prompt_type)
                VALUES (?, ?, ?, ?)
            ''', (query_id, selected_model, json.dumps(structured_output), prompt_type))

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

    # API endpoint to get conversation history
    @app.route('/api/history', methods=['GET'])
    def get_history():
        return jsonify({'history': conversation_history})

    # API endpoint to clear conversation history
    @app.route('/api/clear', methods=['POST'])
    def clear_history():
        conversation_history.clear()
        return jsonify({'message': 'History cleared'})

    # Test GlobalGiving API (from previous code)
    @app.route('/api/test-globalgiving')
    def test_globalgiving():
        """Test if GlobalGiving API is working"""
        try:
            base_url = "https://api.globalgiving.org/api/public/services/search/project/summary"

            params = {
                'q': 'education',
                'start': 0,
                'nexus': 'json'
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
                    'total_projects': data.get('search', {}).get('numberFound', 0),
                    'sample_data': data
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


if __name__ == '__main__':
    app = create_app()
    print("Starting Altrue Chatbot...")
    print("Open your browser to: http://127.0.0.1:5000/")
    app.run(debug=True)