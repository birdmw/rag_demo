import streamlit as st
from typing import List
from tempfile import TemporaryDirectory
from data_wrangler import *
from openai_client import *

class Manager:

    _db_cursor = None
    _openai_client = None
    _rag_check_box = False

    def __init__(self) -> None:
        self.db_manager = DataWrangler()
        self.client = Gpt()

    #--------- Load UI -----------------------
    def display_prompt_ui(self):
        st.markdown("<h1 style='text-align: center; color: white;'>Premera AI Assist</h1>", unsafe_allow_html=True)

        self._rag_check_box = st.sidebar.checkbox('Rag support ?')

       # user_question = st.chat_input('Question')
        data_file = st.sidebar.file_uploader("Data file",type=['.pdf'])

    

    def compile(self, user_message, max_chunk_length=500):
     #   if not self._rag_check_box:        
     #       return self.client.chat.completions.create(
     #           model="gpt-4",
     #           messages=[
     #              {"role": "system", "content": "You are a AI assistant, skilled in explaining complex programming concepts with creative flair."},
     #               {"role": "user", "content": user_message}
     #           ])
        relevant_chunks = self.db_manager.retrieve_chunks(user_message)
        combined_context = " ".join([chunk[0][:max_chunk_length] for chunk in relevant_chunks])
        return self.client.generate(combined_context, user_message)