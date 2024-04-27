#app/__init__.py
import sys
import os

# Get the absolute path of the project's root directory (using forward slashes)
project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Add the root directory to the Python path
sys.path.insert(0, project_root)

# Flask application initialization
from flask import Flask
from .routes.views import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.settings')  # Assuming you have a settings class in config.py

    # Register blueprints or routes here
    register_routes(app)

    # ... (other initialization logic if needed) ...

    return app