from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import requests
import json

# Load environment variables from .env
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Root route
    @app.route('/')
    def home():
        return "API working ✅"

    # Test GlobalGiving API connection
    @app.route('/test-globalgiving')
    def test_globalgiving():
        """Test if GlobalGiving API is working"""
        try:
            # GlobalGiving public search endpoint
            base_url = "https://api.globalgiving.org/api/public/services/search/project/summary"

            # Test with a simple query
            params = {
                'q': 'education',  # Search for education projects
                'start': 0,  # Start from first result
                'nexus': 'json'  # Request JSON format
            }

            headers = {
                'Accept': 'application/json',
                'User-Agent': 'AltrueBot/1.0'
            }

            response = requests.get(base_url, params=params, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Extract key info from response
                result = {
                    'status': 'success',
                    'total_projects': data.get('search', {}).get('numberFound', 0),
                    'projects_returned': len(data.get('search', {}).get('projects', {}).get('project', [])),
                    'sample_project': None
                }

                # Get first project as sample
                projects = data.get('search', {}).get('projects', {}).get('project', [])
                if projects:
                    first_project = projects[0]
                    result['sample_project'] = {
                        'id': first_project.get('id'),
                        'title': first_project.get('title'),
                        'summary': first_project.get('summary', '')[:200] + '...',
                        'country': first_project.get('country'),
                        'theme': first_project.get('theme'),
                        'url': first_project.get('projectLink')
                    }

                return jsonify(result)
            else:
                return jsonify({
                    'status': 'error',
                    'message': f'API returned status code: {response.status_code}',
                    'response': response.text
                }), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify({
                'status': 'error',
                'message': f'Request failed: {str(e)}'
            }), 500
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Unexpected error: {str(e)}'
            }), 500

    # Test different search queries
    @app.route('/search/<topic>')
    def search_by_topic(topic):
        """Search GlobalGiving by topic"""
        try:
            base_url = "https://api.globalgiving.org/api/public/services/search/project/summary"

            params = {
                'q': topic,
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
                projects = data.get('search', {}).get('projects', {}).get('project', [])

                # Format projects for easy reading
                formatted_projects = []
                for project in projects[:5]:  # Limit to first 5
                    formatted_projects.append({
                        'id': project.get('id'),
                        'title': project.get('title'),
                        'country': project.get('country'),
                        'theme': project.get('theme'),
                        'summary': project.get('summary', '')[:150] + '...' if len(
                            project.get('summary', '')) > 150 else project.get('summary', ''),
                        'url': project.get('projectLink')
                    })

                return jsonify({
                    'status': 'success',
                    'topic': topic,
                    'total_found': data.get('search', {}).get('numberFound', 0),
                    'projects': formatted_projects
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

    # Test with country filter
    @app.route('/search/<topic>/<country>')
    def search_by_topic_and_country(topic, country):
        """Search GlobalGiving by topic and country"""
        try:
            base_url = "https://api.globalgiving.org/api/public/services/search/project/summary"

            params = {
                'q': topic,
                'country': country,
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
                projects = data.get('search', {}).get('projects', {}).get('project', [])

                # Format projects
                formatted_projects = []
                for project in projects[:3]:  # Limit to first 3
                    formatted_projects.append({
                        'id': project.get('id'),
                        'title': project.get('title'),
                        'country': project.get('country'),
                        'theme': project.get('theme'),
                        'summary': project.get('summary', '')[:200] + '...' if len(
                            project.get('summary', '')) > 200 else project.get('summary', ''),
                        'url': project.get('projectLink')
                    })

                return jsonify({
                    'status': 'success',
                    'search_params': f"{topic} in {country}",
                    'total_found': data.get('search', {}).get('numberFound', 0),
                    'projects': formatted_projects
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
    print("🚀 Starting Flask app...")
    print("📍 Test URLs:")
    print("   - Basic test: http://127.0.0.1:5000/")
    print("   - GlobalGiving test: http://127.0.0.1:5000/test-globalgiving")
    print("   - Search by topic: http://127.0.0.1:5000/search/education")
    print("   - Search by topic+country: http://127.0.0.1:5000/search/education/kenya")
    app.run(debug=True)