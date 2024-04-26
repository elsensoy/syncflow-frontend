from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from .video_processing import process_video
from .utils.api_utils import generate_content_from_frames
from .utils.error_handling import InvalidUsage

app = Flask(__name__)

# Assuming you have a config.py with a get_config() function
from .config import get_config
config = get_config()

# Allowed video file extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_video():
    # Check if a video file was uploaded
    if 'video' not in request.files:
        raise InvalidUsage('No video file provided.', status_code=400)
    video = request.files['video']

    # Validate filename and extension
    if video.filename == '':
        raise InvalidUsage('Empty filename.', status_code=400)
    if not allowed_file(video.filename):
        raise InvalidUsage('Invalid file format.', status_code=400)

    # Secure filename before processing
    filename = secure_filename(video.filename)

    try:
        # Process video and extract frames (async implementation example)
        frames_uris = process_video.delay(video, filename)

        # Return a response indicating processing has started
        return jsonify({
            'message': 'Video processing started.',
            'task_id': frames_uris.id  # Assuming an async task ID is returned
        })

    except Exception as e:
        # Handle processing errors
        raise InvalidUsage('Video processing failed.', status_code=500)

# ... (Add routes to check status and retrieve results based on task_id) ...

if __name__ == '__main__':
    app.run(debug=True)