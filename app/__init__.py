import sys
import os

# Get the absolute path of the project's root directory
project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Add the root directory to the Python path (if necessary)
sys.path.insert(0, project_root)

# Flask application initialization
from flask import Flask
from routes.views import register_routes  # Absolute import
from config.settings import Config  # Absolute import

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from Config class

    # Register blueprints or routes
    register_routes(app)

    # ... (other initialization logic if needed) ...

    return app