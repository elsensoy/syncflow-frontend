import google.generativeai as genai

def upload_frame(frame_path):
    with open(frame_path, 'rb') as file:
        response = genai.upload_file(file=file, file_name=os.path.basename(frame_path))
        return response.uri

def generate_content_from_frames(frame_uris, prompt):
    parts = [{'text': prompt}]
    for uri in frame_uris:
        parts.append({'fileData': {'fileUri': uri, 'mimeType': 'image/jpeg'}})
    response = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest").generate_content(parts)
    return response.text
