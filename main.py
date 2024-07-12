from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv
from utils import (
    extract_details,
    TaskDetails,
    extract_audio
)
import os
from logging.config import dictConfig
from logconfig import log_config
import logging

dictConfig(log_config)

load_dotenv()

app = FastAPI(debug=True)

logger = logging.getLogger("exTaskAutomation-logger")

@app.get("/")
def read_root():
    return {"Status": "Working"}

@app.post("/extract_task_entity_from_text", response_model=TaskDetails)
async def extract_task_entities(task: any):   
    #task: str = "Hi, this is Arun with a quick update on my current task status. Today we discussed about a task S456 for more than 30 minutes and its expected end is today."
    # entities = extract_details(task)
    # entities.text = task
    return task

@app.post("/extract_task_entity_from_audio", response_model=TaskDetails)
async def extract_task_entities(
    audio_file: UploadFile = File(...)
    ):
    # save the audio file
    file_extension = audio_file.filename.split(".")[-1]
    tempfile = f"res/audio_file.{file_extension}"
    with open(tempfile, "wb") as f:
        f.write(audio_file.file.read())
    task = extract_audio(tempfile)    

    # if os.path.exists(tempfile):
    #    os.remove(tempfile)

    entities = extract_details(task)
    entities.text = task
    return entities
