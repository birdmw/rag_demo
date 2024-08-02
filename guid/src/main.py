import streamlit as st
from manager import *
from data_wrangler import *

st.set_page_config(page_title="Prompting", page_icon=":robot_face:", layout="wide")

gui_manager = Manager()
db_manager = DataWrangler()

@st.cache_resource
def initialize_gui():
    db_manager.initialize()

st.sidebar.write('## Select File')
gui_manager.display_prompt_ui()

if "chatting_messages" not in st.session_state:
    st.session_state["chatting_messages"] = [
            {
                "role":"assistant", 
                "content":"Welcome, I'm Premera's agent! How can I assist you today?", 
                "question":''
            }]

for ms in st.session_state.chatting_messages:
    if ms["question"] != '': # handle Initial load 
        st.chat_message("user").write(ms["question"])    
    st.chat_message(ms["role"]).write(ms["content"])

if chat := st.chat_input("How can I assist you today?", key="user_input"):
    #question = [{"role":"user", "content":chat}]
    st.chat_message("user").write(chat)

    # show busy cursor, chat completion will take some time to process the request.
    with st.spinner('GPT model processing your request..'):
        extractAnswer = gui_manager.compile(user_message=chat)
    
    # response from model can be empty for prompt like "thank you"
    if extractAnswer != '':
        answer = {"role":"assistant", "content":extractAnswer, "question": chat}    
        st.chat_message("assistant").write(extractAnswer)
        st.session_state.chatting_messages.append(answer)



#####################################
#   
#   streamlit run .\main.py
#
#######################################