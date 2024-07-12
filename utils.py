from datetime import datetime
from openai import OpenAI
from typing import Literal, Optional, Type
from mirascope.openai import OpenAIExtractor
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv() 

class TaskDetails(BaseModel):
    text: str
    task: str
    status: Literal["todo", "in-progress", "in-review", "completed"]
    duration: str  
    #start: Optional[datetime] = Field(None, title='start date', ge=datetime.min, le=datetime.max, default_factory = datetime.utcnow)   
    start: Optional[datetime]
    end: Optional[datetime] 
    priority: Literal["low", "normal", "high"]

class TaskExtractor(OpenAIExtractor[TaskDetails]):
    extract_schema: Type[TaskDetails] = TaskDetails
    prompt_template = """
    Extract the task details from the following task:
    {task}
    """
    task: str

class TaskInfo(BaseModel):
    text:str = ''
    def serialize(self):
        if self.text is not None:
            return {"text": self.text}        

class APIInput:
    url: str
    method: str = 'GET'
    fileInfo: any
    data: any

    def __init__(self, url: str, method: str = None):
        self.url = url

        if method is not None:           
            self.method = method

    @classmethod
    def using_fileInfo(cls, url: str, method: str, fileInfo):
        cls.fileInfo = fileInfo
        return cls(url, method)
    
    @classmethod
    def using_data(cls, url: str, method: str, data: any):
        cls.data = data.serialize()
        return cls(url, method)

class APIResponse:
    success: bool
    resultJSON: any
    content: any
    resultText: str
    statusCode: int

def extract_details(task: str) -> TaskDetails:
    try:
        task_details = TaskExtractor(task=task).extract()
        return task_details
    except Exception as e:
        return ("[Exception in extract_details]: ", e)
    
def extract_audio(file_path) -> TaskDetails:
    try:        
        client = OpenAI()
        audio_file = open(file_path, "rb")    
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcription.text
    except Exception as e:
        return ("[Exception in extract_audio]: ", e)
        
