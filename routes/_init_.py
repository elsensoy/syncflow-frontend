from flask import Flask, request, jsonify
from .video_processing import process_video
from .utils.api_utils import generate_content_from_frames

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_video():
    video = request.files['video']
    # Process video and extract frames
    # Assume you save frames locally and then upload to API
    frames_uris = process_video(video)
    # Generate content
    text = generate_content_from_frames(frames_uris, "Describe this video.")
    return jsonify({'description': text})

if __name__ == '__main__':
    app.run(debug=True)

