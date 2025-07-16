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

    # Store conversation history (in production, use a database)
    conversation_history = []

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

            if not user_message:
                return jsonify({'error': 'No message provided'}), 400

            # Add user message to history
            conversation_history.append({
                'type': 'user',
                'message': user_message,
                'timestamp': datetime.now().isoformat()
            })

            # Mock response for now (replace with actual GlobalGiving + OpenAI integration)
            if selected_model == 'gpt-3.5-turbo':
                bot_response = f"🤖 GPT-3.5 Response: I found several charities related to '{user_message}'. Here are my recommendations based on impact and transparency."
            else:
                bot_response = f"🧠 GPT-4 Response: After analyzing '{user_message}', I recommend these high-impact organizations with detailed reasoning."

            # Add bot response to history
            conversation_history.append({
                'type': 'bot',
                'message': bot_response,
                'model': selected_model,
                'timestamp': datetime.now().isoformat()
            })

            return jsonify({
                'response': bot_response,
                'model': selected_model,
                'timestamp': datetime.now().isoformat()
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
    print("🚀 Starting Altrue Chatbot...")
    print("📍 Open your browser to: http://127.0.0.1:5000/")
    app.run(debug=True)