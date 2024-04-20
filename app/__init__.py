# /my-flask-app/app/__init__.py
from flask import Flask
from .routes.views import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.settings')

    register_routes(app)

    return app
