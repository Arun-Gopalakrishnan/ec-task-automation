from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv
from utils import (
    extract_details,
    TaskDetails,
    extract_audio
)
import os

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Status": "Working"}

@app.post("/extract_task_entities", response_model=TaskDetails)
async def extract_task_entities(
    audio_file: UploadFile = File(...)
    ):
    # save the audio file
    file_extension = audio_file.filename.split(".")[-1]
    tempfile = f"res/audio_file.{file_extension}"
    with open(tempfile, "wb") as f:
        f.write(audio_file.file.read())
    text = extract_audio(tempfile)

    if os.path.exists(tempfile):
        os.remove(tempfile)

    entities = extract_details(text)
    return entities
