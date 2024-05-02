import os
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import asyncio
import websockets
import json
from google.cloud import speech
from .video_processing import generate_frames  # Assuming you have your video processing logic
# ... other imports ...
from .routes.views import register_routes
from .speech_recognition import create_speech_client, recognize_speech

load_dotenv()
app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')  # Use threading for async support
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set in .env file")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/wsl.localhost/Ubuntu/home/elidasensoy/my_flask_app/secrets/nemo-init-ca43e0ad082e.json"


# Google Cloud Speech client initialization
speech_client = speech.SpeechClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

async def recognize_speech(audio_data):
    # ... (Implement your Google Cloud Speech-to-Text logic here) ...
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )
    response = speech_client.recognize(config=config, audio=audio_data)
    transcript = " ".join(result.alternatives[0].transcript for result in response.results)
    return transcript

async def handle_audio_data(websocket, path):
    audio_chunks = []
    while True:
        try:
            data = await websocket.recv()
            audio_chunks.append(data)
            # ... (Logic to accumulate audio chunks based on size or duration) ...
            if enough_data_for_recognition:
                # Create speech client and streaming config (moved here for efficiency)
                client, streaming_config = create_speech_client()  
                transcript = await recognize_speech(client, streaming_config, audio_chunks)
                await socketio.emit('update_transcript', {'transcript': transcript}, namespace='/')
                audio_chunks = []
        except websockets.exceptions.ConnectionClosed:
            break

@socketio.on('start_recording', namespace='/')
def start_recording(data):
    print("Started recording")
    # ... (Optional: Start any additional recording processes) ...

@socketio.on('stop_recording', namespace='/')
def stop_recording():
    print("Stopped recording")
    # ... (Optional: Stop and clean up recording processes) ...

if __name__ == '__main__':
    start_server = websockets.serve(handle_audio_data, "localhost", 8765)  # Adjust port as needed
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    socketio.run(app, debug=True)