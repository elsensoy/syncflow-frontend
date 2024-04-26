from flask import Blueprint, request, jsonify
from ..services.video_processing import process_video
from ..utils.error_handling import InvalidUsage

views = Blueprint('views', __name__)

@views.route('/process_video', methods=['POST'])
def handle_video_processing():
    try:
        # Check if a video file was uploaded
        if 'video' not in request.files:
            raise InvalidUsage('No video file provided.', status_code=400)
        video_file = request.files['video']

        # Validate filename and extension (add allowed extensions check)
        # ...

        # Process video (async implementation example)
        result = process_video.delay(video_file)

        # Return a response indicating processing has started
        return jsonify({
            'message': 'Video processing started.',
            'task_id': result.id  # Assuming an async task ID is returned
        })

    except InvalidUsage as e:
        return jsonify({'error': e.message}), e.status_code

    except Exception as e:
        # Handle processing errors
        return jsonify({'error': 'Video processing failed.'}), 500

def register_routes(app):
    app.register_blueprint(views)