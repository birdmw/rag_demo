import streamlit as st
from typing import List
from tempfile import TemporaryDirectory
from data_wrangler import *
from openai_client import *
from user_client import *

class Manager:

    _db_cursor = None
    _openai_client = None
    _rag_check_box = False
    _authenticated = False 

    def __init__(self) -> None:
        self.db_manager = DataWrangler()
        self.client = Gpt()
        self.user_client = User()

    #--------- Load UI -----------------------
    def display_prompt_ui(self):
        st.markdown("<h1 style='text-align: center; color: white;'>PremeraGPT</h1>", unsafe_allow_html=True)
        self._rag_check_box = st.sidebar.checkbox('RAG')
        self._authenticated = st.sidebar.checkbox('Authenticated') 
        
    def __display_text_box(self, context, authenticated):
        if authenticated:
            st.sidebar.text_area("User Infomration:", self.user_client.get_user_data(), height=300)  
        st.sidebar.text_area("Document Reference:", context, height=500)            

    def compile(self, user_message, max_chunk_length=500):
        if not self._rag_check_box:        
            return self.client.rag_checkbox(user_message)
        
        relevant_chunks = self.db_manager.retrieve_chunks(user_message)
        combined_context = " ".join([chunk[0][:max_chunk_length] for chunk in relevant_chunks])
        self.__display_text_box(combined_context, self._authenticated)
        return self.client.generate(combined_context, user_message, self._authenticated)