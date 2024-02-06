from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from google.generativeai import GenerativeModel
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# fuction to load  gemini pro model and get response
model=genai.GenerativeModel("gemini-pro")

chat=model.start_chat(history=[])

def get_gemini_response(questions):
    response=chat.send_message(questions,stream=True)
    return response

# initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# initialize  session state for chat history if it doesnot exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]
    
input=st.text_input("Input:",key="input")
submit=st.button("Ask the question")

if submit and input:
    response=get_gemini_response(input)   
    #  add user query and response to session chat history    
    st.session_state['chat_history'].append(('you',input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot",chunk.text))
        
st.subheader("The Chat History is")
for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")