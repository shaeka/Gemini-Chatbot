# Gemini-Project
A streamlit app that uses Gemini Pro and Gemini Pro Vision in a chatbot interface.

The deployed app can be accessed [here](https://gemini-project-chatbot.streamlit.app/)

# How to get your Gemini Pro API key:
Follow the instruction [here](https://ai.google.dev/pricing) to get your free API key

# Instruction on how to use this app locally
1. Download the file
2. Extract the file
3. Open up notepad, key in the following details and save the file as .env inside the extracted folder
```
GOOGLE_API_KEY="YOUR_API_KEY"
```
4. Open up anaconda prompt or command prompt and activate anaconda environment
5. Create a new conda environment
```
conda create --name new_env python==3.10 -y
```
6. Activate the environment
```
conda activate new_env
```
7. Change directory to the location of the extracted folder (e.g. in Downloads)
```
cd C:/Users/enter_your_user/Downloads/extracted_filename
```
8. Install the required libraries
```
pip install -r requirements.txt
```
9. Run streamlit app
```
streamlit run app.py
```

# Credits:
Credits to Krish Naik for going through Gemini Pro API in this [video](https://www.youtube.com/watch?v=W0rNUAfqGFc&list=PLZoTAELRMXVNbDmGZlcgCA3a8mRQp5axb&index=3).
Watching this video has given me the idea to build this application. 
