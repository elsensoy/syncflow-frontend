#app.py (main file)
from flask import Flask, render_template, Response
from dotenv import load_dotenv  # Import the load_dotenv function from python-dotenv
import os  # Import the os module to access environment variables

load_dotenv()  # This will load environment variables from .env file into the environment

from .video_processing import generate_frames  # Import the function from video_processing module

app = Flask(__name__)

# Access your API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set in .env file")

@app.route('/')
def index():
    # Render an HTML page that includes the video stream
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Stream the video frames as a multipart response
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
