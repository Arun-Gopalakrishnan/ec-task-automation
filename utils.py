from datetime import date
from openai import OpenAI
from typing import Literal, Optional, Type
from mirascope.openai import OpenAIExtractor
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class TaskDetails(BaseModel):
    task: str
    status: Literal["todo", "in-progress", "in-review", "completed"]
    duration: str
    start: Optional[date] = Field(None, title='task start date', ge=date.min, le=date.max)    
    enddate: Optional[date] = Field(None, title='task end date', ge=date.min, le=date.max)    
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

def extract_audio(file_path) -> str:
    try:
        client = OpenAI()
        audio_file = open(file_path, "rb")    
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return "{ apiKey: %s, project: %s, organization:%s }" % (client.api_key, client.project, client.organization)
    except Exception as e:
        return ("[Exception in extract_audio]: ", e)
