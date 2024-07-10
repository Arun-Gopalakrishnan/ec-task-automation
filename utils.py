from click import DateTime
from openai import OpenAI
from typing import Literal, Type
from mirascope.openai import OpenAIExtractor
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class TaskDetails(BaseModel):
    task: str
    status: Literal["todo", "in-progress", "in-review", "completed"]
    duration: str
    start: str
    end: str    
    priority: Literal["low", "normal", "high"]


class TaskExtractor(OpenAIExtractor[TaskDetails]):
    extract_schema: Type[TaskDetails] = TaskDetails
    prompt_template = """
    Extract the task details from the following task:
    {task}
    """
    task: str


def extract_details(task: str) -> TaskDetails:
    task_details = TaskExtractor(task=task).extract()
    return task_details


def extract_audio(file_path):
    client = OpenAI()

    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format="text"
    )
    return transcription.text
