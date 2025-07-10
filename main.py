from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Root route
    @app.route('/')
    def home():
        return "API working ✅"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
