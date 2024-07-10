from dotenv import load_dotenv
import requests
import os

load_dotenv()

EXTRACT_TASK_ENTITIES_URI = 'https://ec-task-automation.streamlit.app/extract_task_entities'
EXTRACT_TEXT_FROM_AUDIO_URI = 'https://ec-task-automation.streamlit.app/extract_text_from_audio'

def get_fileInfo(file):
    return {"audio_file": (file.name, file, 'multipart/form-data')}

def get_api_response(URI, file):
    response = response = requests.post(
        URI,
        files = get_fileInfo(file)
    )
    return response

def extract_task_entities(file):
    return get_api_response(EXTRACT_TASK_ENTITIES_URI, file)

def extract_text_from_audio(file):
    return get_api_response(EXTRACT_TEXT_FROM_AUDIO_URI, file)
