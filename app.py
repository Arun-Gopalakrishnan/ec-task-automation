import json
from pydantic import BaseModel
import streamlit as st
from streamlit_utils import extract_from_audio, extract_from_text
from logging.config import dictConfig
from logconfig import log_config
import logging
import requests
from typing import TypeVar, Type
from utils import APIResponse
from utils import (
    TaskInfo,
    APIResponse
)

dictConfig(log_config)
logger = logging.getLogger("exTaskAutomation-logger")

st.title("EC - Task Automation")

supported_files = ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']

uploaded_file = st.file_uploader("Upload your file", type=supported_files)
use_whisper = st.checkbox("Use Whisper", value=True, disabled=True)
#use_whisper = st.radio("Use Whisper", value=True, disabled=True)
task = st.text_area("Task:", placeholder="Enter your text here!", height=200, max_chars=250)

T = TypeVar('T')

def showErrorInfo(err: T):
    st.error(f"Failed to extract entity from audio file!")
    st.write('Exception:')
    if type(err) == Exception:
        exp = Exception(err)
        st.write(exp)
    else:
        msg = str(err)
        st.write(msg)

def showOutput(res: APIResponse):
    if res.success:                            
        st.success(f"Entity extracted Successfully!")
        st.write('Task Details:')
        st.write(res.resultJSON)      
    else:
        showErrorInfo(res.resultText)
        st.write(f"status code: {res.statusCode}")
        st.write(f"content: {res.content}")

if st.button('Extract Entities'):
    if uploaded_file is not None:
        st.write("Filename:", uploaded_file.name)
        st.write("Filetype:", uploaded_file.type)
        
        with st.spinner(f"Parsing the file - {uploaded_file.name}..."):
            if uploaded_file is not None:
                try:
                    res = extract_from_audio(
                                            uploaded_file
                                        )                  
                    showOutput(res)
                except Exception as e:
                    showErrorInfo(e)
    elif task.count(task) > 0:
        try:
            taskInfo = TaskInfo()
            taskInfo.text = task
            res = extract_from_text(
                                    taskInfo
                                )
            showOutput(res)
        except Exception as e:
            showErrorInfo(e)


