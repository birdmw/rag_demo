import streamlit as st
from typing import List
from tempfile import TemporaryDirectory
from data_wrangler import *
from openai_client import *
from chunker import *

class Manager:

    _db_cursor = None
    _openai_client = None
    _rag_check_box = False
    _authenticated = False 

    def __init__(self) -> None:
        self.db_manager = DataWrangler()
        self.client = Gpt()
        self.chunk_manager = Chunker()
       
    #--------- Load UI -----------------------
    def display_prompt_ui(self):
        st.markdown("<h1 style='text-align: center; color: white;'>Premera AI Assist</h1>", unsafe_allow_html=True)
        self._rag_check_box = st.sidebar.checkbox('RAG')
        self._authenticated = st.sidebar.checkbox('Authenticated') 
        
       # data_file = st.sidebar.file_uploader("Data File",type=['.txt'])
        # Read the file contents
       # if data_file:
       #     file_contents = data_file.read()
            # Convert the contents to a string (assuming the file is a text file)
       #     file_text = file_contents.decode("utf-8")
       ##     st.write(file_text)
        #    self.chunk_file(file_text)            
        
       
    def chunk_file(self, text):
        chunks = self.chunk_manager.read_and_chunk_file(text)
        pyramid = self.chunk_manager.create_summary_pyramid(chunks)
        self.chunk_manager.insert_layers(pyramid)

    def compile(self, user_message, max_chunk_length=500):
        if not self._rag_check_box:        
            return self.client.rag_checkbox(user_message)
        
        relevant_chunks = self.db_manager.retrieve_chunks(user_message)
        combined_context = " ".join([chunk[0][:max_chunk_length] for chunk in relevant_chunks])
        return self.client.generate(combined_context, user_message, self._authenticated)