from dotenv import load_dotenv
import requests
import os

load_dotenv()

# EXTRACT_URI = 'https://ec-task-automation.streamlit.app/extract_task_entities'
EXTRACT_URI = 'https://fastapi-example-p197.onrender.com/extract_task_entities'

def get_api_response(file):
    response = response = requests.post(
        EXTRACT_URI,
        files={"audio_file": (file.name, file, 'multipart/form-data')}
    )
    return response.text
