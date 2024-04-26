#video_processing.py
import cv2
from .model import gesture_model

def preprocess(frame):
    # Example preprocessing: resizing and normalization
    frame_resized = cv2.resize(frame, (224, 224))  # Adjust size as necessary
    frame_normalized = frame_resized / 255.0
    return frame_normalized

def recognize_gestures(frame):
    # Use the gesture model to predict gestures in the frame
    return gesture_model.predict(frame)

def generate_frames():
    cap = cv2.VideoCapture(0)  # Use the default camera
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = preprocess(frame)
            gesture_results = recognize_gestures(processed_frame)
            annotated_frame = annotate_frame(frame, gesture_results)

            _, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    finally:
        cap.release()

def annotate_frame(frame, results):
    # Annotate the frame based on gesture results
    for result in results:
        # Add annotations (e.g., bounding boxes, labels)
        cv2.rectangle(frame, (result['x'], result['y']), (result['x'] + result['width'], result['y'] + result['height']), (0, 255, 0), 2)
        cv2.putText(frame, result['label'], (result['x'], result['y'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    return frame
