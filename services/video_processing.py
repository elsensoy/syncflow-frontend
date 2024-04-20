import cv2
import numpy as np
from .model.load_model import get_model

model = get_model()

def process_video_frame(video_data):
    # Convert byte data to numpy array
    nparr = np.fromstring(video_data, np.uint8)
    # Decode image
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Preprocess and predict using model
    # This is a simplification. You'll likely need to handle batching and more.
    processed_frame = preprocess(frame)
    result = model(processed_frame)
    return result

def preprocess(frame):
    # Resize, normalize, etc.
    # Convert frame to tensor, etc.
    return frame
