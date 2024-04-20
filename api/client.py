# /my_flask_app/app/api/client.py

import requests

def generate_content(api_key, content_url, image_uris):
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {
        'uris': image_uris,
        'model': 'gemini-1.5-pro-latest',
        'prompt': 'Describe this video.'
    }
    response = requests.post(content_url, json=data, headers=headers)
    return response.json()

