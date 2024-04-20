# upload_frames.py
import requests

def upload_frame(api_key, frame_path, upload_url):
    headers = {'Authorization': f'Bearer {api_key}'}
    with open(frame_path, 'rb') as f:
        files = {'file': (frame_path, f)}
        response = requests.post(upload_url, files=files, headers=headers)
    return response.json()

# Example of using the function
if __name__ == "__main__":
    from config import get_api_key
    api_key = get_api_key()
    response = upload_frame(api_key, "frames_output_directory/frame_0.jpg", "https://api.example.com/upload")
    print("Upload response:", response)
