from dotenv import load_dotenv
import requests
import os

load_dotenv()

EXTRACT_TASK_ENTITIES_URI = 'https://ec-task-automation.streamlit.app/extract_task_entities'
EXTRACT_TEXT_FROM_AUDIO_URI = 'https://ec-task-automation.streamlit.app/extract_text_from_audio'

def get_api_response(file):
    response = response = requests.post(
        EXTRACT_TASK_ENTITIES_URI,
        files={"audio_file": (file.name, file, 'multipart/form-data')}
    )
    return response.json()

def get_api_response_as_text(file):
    response = response = requests.post(
        EXTRACT_TEXT_FROM_AUDIO_URI,
        files={"audio_file": (file.name, file, 'multipart/form-data')}
    )
    return response.text
