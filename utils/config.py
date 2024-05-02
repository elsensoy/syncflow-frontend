# /utils/config.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load all the environment variables from a .env file

def get_api_key():
    return os.getenv("GOOGLE_API_KEY")

# Example of using the function
if __name__ == "__main__":
    api_key = get_api_key()
    print("API Key:", api_key)
