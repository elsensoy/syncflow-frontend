# /my-flask-app/config/settings.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    API_BASE_URL = 'https://api.example.com/'

# You can have different classes for dev and production setups if needed.
