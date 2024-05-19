# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 10:12:47 2023
Note: "./.streamlit/config.toml" is used to remove the automatically generated sidebar by streamlit.
@author: kuany
"""
### Loading all the environmental variables
from dotenv import load_dotenv
load_dotenv() 
import os
from PIL import Image
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

text_model = genai.GenerativeModel('gemini-pro')
image_model = genai.GenerativeModel('gemini-pro-vision')

chat = text_model.start_chat(history=[])

### Create a function to load Gemini Pro model and get responses
def get_gemini_response(model_option, question = None, image_input = None):
    """
    Get gemini response given question/image
    
    Input:
    - User question in text
    - Image if any
    Output:
    - Gemini model's response in text
    """
    if model_option == 'Yes':
        model = image_model
        if question != '':
            response = model.generate_content([question, image_input])
        else:
            response = model.generate_content(image_input)
    else:
        response = chat.send_message(question)
        
    return response.text

### Initialize our streamlit app, keep sidebar collapsed
st.set_page_config(page_title = 'Gemini Project', layout='wide', initial_sidebar_state='collapsed')

st.header('Gemini Pro / Gemini Pro Vision')

### Setup multi pages application, reference: https://docs.streamlit.io/develop/tutorials/multipage/st.page_link-nav
st.sidebar.page_link('app.py', label='Main Page')
st.sidebar.page_link('pages/audio_to_text_summarization.py', label='Audio to Text Summarization')
st.sidebar.page_link('pages/generate_cover_letter.py', label='Cover Letter Generator')
st.sidebar.page_link('pages/multi_documents_QA.py', label='Multi-Documents Q&A')

col1, col2 = st.columns(2)

with col1:

    model_option = st.selectbox('Do you need to provide image for your question?', 
                                ('No', 'Yes'))
        
    if 'model_option' not in st.session_state:
        st.session_state.model_option = ''
        st.session_state.model_option = model_option
    
    if 'submit_button' not in st.session_state:
        st.session_state.submit_button = ''
        st.session_state.input = ''
        st.session_state.clicked = False
        st.session_state.question_log = []
        st.session_state.response_log = []
        st.session_state.image_log = []
    
    if st.session_state.model_option != model_option:
        st.session_state.submit_button = ''
        st.session_state.input = ''
        st.session_state.clicked = False
        st.session_state.model_option = model_option
    
    image = ''
    input = st.text_area('Input: ', key='input')
    
    if model_option == 'Yes':
        uploaded_file = st.file_uploader('Choose an image', type=['jpg', 'jpeg', 'png'])
        image = ''
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
    
    ### When submit is clicked
    if st.button("Generate response"):
        st.session_state.question_input = input
        
        if image != '':
            response = get_gemini_response(model_option, st.session_state.question_input, image)
        else:
            response = get_gemini_response(model_option, st.session_state.question_input)
        
        st.subheader('Current question asked:')
        ### Add in "User" icon beside the question
        st.chat_message('User').write(st.session_state.question_input)
        
        if image != '':
            temp_image = st.empty()
            ### Add in "User" icon beside the question
            st.chat_message('User').image(image, caption='Uploaded Image', use_column_width=True)
        
        st.subheader('Current response is')
        ### Add in "AI" icon beside the question
        st.chat_message('AI').write(response)
        st.session_state.question_log.append(st.session_state.question_input)
        st.session_state.image_log.append(image)
        st.session_state.response_log.append(response)
    else:
        if image != '':
            temp_image = st.image(image, caption='Uploaded Image', use_column_width=True)

with col2:
    st.subheader('Past Questions and Responses:')
    if st.button('Clear past responses'):
        st.session_state.question_log, st.session_state.image_log, st.session_state.response_log = [], [], []
    for index, (each_question, each_image, each_response) in enumerate(zip(st.session_state.question_log, st.session_state.image_log, st.session_state.response_log)):
        st.subheader('Question {}:'.format(index + 1))
        ### Add in "User" icon beside the question
        st.chat_message('User').write(each_question)
        
        if each_image != '':
            ### Add in "User" icon beside the question
            st.chat_message('User').image(each_image)
        
        st.subheader('Response {}:'.format(index + 1))
        ### Add in "AI" icon beside the question
        st.chat_message('AI').write(each_response)
    
    st.session_state.question_input = ''