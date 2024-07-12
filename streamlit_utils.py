from typing import Iterable, Mapping
from dotenv import load_dotenv
import requests
from utils import (
    APIInput,
    APIResponse
)
from constants import (
    EXTRACT_FROM_AUDIO_URI,
    EXTRACT_FROM_TEXT_URI
)

load_dotenv()

def compose_response_obj(response: requests.Response) -> APIResponse:       
    res = APIResponse()
    res.resultText = response.text
    res.statusCode = response.status_code    
    res.content = response.content
    res.success = (response.status_code.__eq__(200))
    if (res.success):
        res.resultJSON = response.json()
    return res

def get_api_response(apiInput: APIInput):
    if apiInput.method.__eq__("POST"):                  
        if hasattr(apiInput, 'fileInfo') and apiInput.fileInfo is not None:
            response = response = requests.post(
                url = apiInput.url,
                files = apiInput.fileInfo     
            )
        elif hasattr(apiInput, 'data') and apiInput.data is not None:
            response = response = requests.post(
                url = apiInput.url,
                json =  apiInput.data
            )
        else:
            response = response = requests.post(
                url = apiInput.url     
            )
    elif apiInput.method.__eq__("PUT"):
        if hasattr(apiInput, 'fileInfo') and apiInput.fileInfo is not None:
            response = response = requests.put(
                url = apiInput.url,
                files = apiInput.fileInfo     
            )
        elif hasattr(apiInput, 'data') and apiInput.data is not None:
            response = response = requests.put(
                url = apiInput.url,
                json =  apiInput.data
            )
        else:
            response = response = requests.put(
                url = apiInput.url     
            )
    elif apiInput.method.__eq__("DELETE"):
        response = response = requests.delete(
            url = apiInput.url,
        )        
    else:
         response = response = requests.get(
            url = apiInput.url
        )
    return response

def extract_from_audio(file) -> APIResponse:
    try:
        apiInput = APIInput.using_fileInfo(EXTRACT_FROM_AUDIO_URI, "POST", {"audio_file": (file.name, file, 'multipart/form-data')})        
        response = get_api_response(apiInput)
        return compose_response_obj(response)
    except Exception as e:
        raise Exception ("[Exception in extract_from_audio]: ", e)

def extract_from_text(data) -> APIResponse:
    try:        
        apiInput = APIInput.using_data(EXTRACT_FROM_TEXT_URI, "POST", data)        
        response = get_api_response(apiInput)
        return compose_response_obj(response)
    except Exception as e:
        raise Exception ("[Exception in extract_from_text]: ", e)

