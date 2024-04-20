# frame_extractor.py
import cv2
import os

def extract_frames(video_path, output_dir, frame_rate=30):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    vidcap = cv2.VideoCapture(video_path)
    count = 0
    success, image = vidcap.read()
    while success:
        if count % frame_rate == 0:  # Save a frame every 'frame_rate' frames
            frame_path = os.path.join(output_dir, f"frame_{count//frame_rate}.jpg")
            cv2.imwrite(frame_path, image)
        success, image = vidcap.read()
        count += 1
    vidcap.release()

# Example of using the function
if __name__ == "__main__":
    extract_frames("path_to_video.mp4", "frames_output_directory")
