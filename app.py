# app.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Debugging: Print all environment variables to check if they are loaded correctly
print("Environment Variables:", dict(os.environ))

from flask import Flask

app = Flask(__name__)

# Accessing API key to check if it's loaded properly
gemini_api_key = os.getenv('GEMINI_API_KEY')
if not gemini_api_key:
    raise ValueError("API key for Gemini is not set.")

@app.route('/')
def index():
    # Display the API key in the response for debugging (remove in production!)
    return f"The API key is configured: {gemini_api_key}"

if __name__ == '__main__':
    app.run(debug=True)
