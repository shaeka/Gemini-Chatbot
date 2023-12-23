# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 10:12:47 2023

@author: kuany
"""

from dotenv import load_dotenv
load_dotenv() ### Loading all the environmental variables

import streamlit as st
import os
import google.generativeai as genai

from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

text_model = genai.GenerativeModel('gemini-pro')
image_model = genai.GenerativeModel('gemini-pro-vision')

### Create a function to load Gemini Pro model and get responses
def get_gemini_response(model_option, question = None, image_input = None):
    if model_option == 'Yes':
        model = image_model
        if question != '':
            response = model.generate_content([question, image_input])
        else:
            response = model.generate_content(image_input)
    else:
        model = text_model
        response = model.generate_content(question)
    return response.text

### Initialize our streamlit app
st.set_page_config(page_title = 'Gemini Project')

st.header('Gemini Pro / Gemini Pro Vision')

model_option = st.selectbox('Do you need to provide image for your question?', 
                            ('No', 'Yes'))

def reset_options():
    st.session_state.submit_button = ''
    st.session_state.input = ''
    st.session_state.clicked = False

if 'model_option' not in st.session_state:
    st.session_state.model_option = ''
    st.session_state.model_option = model_option

if st.session_state.model_option != model_option or 'submit_button' not in st.session_state:
    reset_options()  
    
def click_button():
    st.session_state.clicked = True
    st.session_state.question_input = st.session_state.input
    st.session_state.input = ''

st.text_input('Input: ', key='input', on_change=click_button)

image = ''

if model_option == 'Yes':
    uploaded_file = st.file_uploader('Choose an image', type=['jpg', 'jpeg', 'png'])
    image = ''
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

submit = st.button('Ask the question', on_click=click_button)

### When submit is clicked
if st.session_state.clicked == True:
    if image != '':
        response = get_gemini_response(model_option, st.session_state.question_input, image)
    else:
        response = get_gemini_response(model_option, st.session_state.question_input)
    st.subheader('The response is')
    st.write(response)
    st.session_state.question_input = ''