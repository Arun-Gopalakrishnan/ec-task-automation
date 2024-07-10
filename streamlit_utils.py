from dotenv import load_dotenv
import requests
import os

load_dotenv()

EXTRACT_URI = 'https://asr-task-automation-ec.onrender.com/extract_task_entities'

def get_api_response(file):
    response = response = requests.post(
        EXTRACT_URI,
        files={"audio_file": (file.name, file, 'multipart/form-data')}
    )
    return response.text
