import streamlit as st
import logging
from streamlit_utils import get_task_entities, get_text_from_audio

logger = logging.getLogger(__name__)

st.title("EC - Task Automation")

supported_files = ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']

uploaded_file = st.file_uploader("Upload your file", type=supported_files)
use_whisper = st.checkbox("Use Whisper", value=True, disabled=True)

if uploaded_file is not None:
    st.write("Filename:", uploaded_file.name)
    st.write("Filetype:", uploaded_file.type)

    if st.button('Extract Entities'):
        with st.spinner(f"Parsing the file - {uploaded_file.name}..."):
            if uploaded_file is not None:
                res = get_api_response(
                        uploaded_file
                    )
                entities_json = res
                st.success(f"Entities extracted Successfully!")
                st.write('Task Details:')
                st.json(entities_json)
