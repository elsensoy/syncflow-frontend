import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Assuming you have SECRET_KEY in .env
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # ... other configuration settings ...

    # Example of accessing a JSON key file path (not recommended to store directly in .env)
    # Assuming you have the path in an environment variable
    JSON_KEY_FILE_PATH = os.environ.get('JSON_KEY_FILE_PATH')  

# ... (other configuration classes if needed) ...