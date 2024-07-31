import os
import streamlit as st

from typing import List
from tempfile import TemporaryDirectory

from openai import OpenAI

import sqlite3
import numpy as np
import os


class Manager:

    _db_cursor = None
    _openai_client = None
    _rag_check_box = False

    def __init__(self) -> None:
        self.system_message  = """You are an AI assistant helping to optimize queries for semantic search. Your task is to rewrite the given query in a way that will improve its semantic matching with relevant document chunks."""
        self.client = OpenAI(api_key='OPEN_API_KEY')
    #--------- Load UI -----------------------
    def display_prompt_ui(self):
        st.markdown("<h1 style='text-align: center; color: white;'>Premera AI Assist</h1>", unsafe_allow_html=True)

        self._rag_check_box = st.sidebar.checkbox('Rag support ?')

       # user_question = st.chat_input('Question')
        data_file = st.sidebar.file_uploader("Data file",type=['.pdf'])
 

    #---------- Load pdf file and chunk ---------------------
    def read_and_chunk_file(self, file_path, chunk_size=500, overlap=100):
        print(f"Reading file: {file_path}")

    def initialize(self):
        # db createion
        conn = sqlite3.connect('../../premera_plan.sql')
        self._db_cursor = conn.cursor()

        self._db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_chunks
            (id INTEGER PRIMARY KEY, content TEXT, embedding BLOB, shape TEXT, layer INTEGER)
            ''')
    
    def compile(self, user_message):
        if not self._rag_check_box:        
            return self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a AI assistant, skilled in explaining complex programming concepts with creative flair."},
                    {"role": "user", "content": user_message}
                ])
        
        