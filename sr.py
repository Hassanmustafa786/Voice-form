import streamlit as st
import pyttsx3
import speech_recognition as sr
from openai import OpenAI
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        st.write("Generating...")
    try:
        user_input = r.recognize_google(audio)
        # st.code(f'YOU: {user_input}')
        return user_input
    except sr.UnknownValueError:
        st.write("Oops, I didn't get your audio, Please try again.")
        return None

def text_to_speech(key, value):
    engine = pyttsx3.init()
    engine.save_to_file(key, f'{str(value)}.mp3')
    engine.runAndWait()
    st.audio(f'{str(value)}.mp3')

# Load API keys from the JSON file
with open(r'D:\OSTF\Chatbot\OPENAI_API_KEY.json') as json_file:
    keys = json.load(json_file)

# Access the ChatGPT API key
chatgpt_api_key = keys['chatgpt']['api_key']

chat = ChatOpenAI(
    temperature=0.5,
    model_name="gpt-3.5-turbo",
    openai_api_key=chatgpt_api_key,
    # max_tokens=50
)

def get_response(user_input):
    intro_message = """You are an AI Assistant. You are a Mental Health Care Expert for OSTF Organization, here to guide and assist people with their health questions and concerns. Please provide accurate and helpful information, and always maintain a polite and professional tone. Your answer should be complete and precise.
                   (Your introductory message here...)"""

    messages = [
        SystemMessage(content=intro_message),
        HumanMessage(content=user_input),
    ]

    response = chat(messages).content

    return response

questions = [
    ("What is your name?", 1),
    ("What are your goals for therapy?", 2),
    ("What brings you to counseling at this time?", 3),
    ("How are you feeling rightnow?", 4),
]

# Initialize the responses using Streamlit's session state
if 'responses' not in st.session_state:
    st.session_state.responses = {}

# Streamlit app
def ask_question():
        st.warning("Refrain from speaking until the *(listening...)* text appears.")
        for i, (question, answer) in enumerate(questions):
            response_key = f"response_{i}"
            if response_key not in st.session_state.responses:
                st.session_state.responses[response_key] = ""

            st.subheader(f"Q{i+1}-  {question}")
        
            if st.button(f"Answer for Question {i + 1}"):
                speak(question)
                user_input = speech_to_text()
                if user_input:
                    st.session_state.responses[response_key] = user_input
                    output = get_response(user_input)
                    v = str(f"{i+1}")
                    text_to_speech(output, v)

            st.divider()
        
def intro():
    speak("Welcome to OSTF Organization. To better assist you, please complete the required information below. Your cooperation ensures swift and precise support tailored to your needs.")


st.set_page_config(layout="wide")
st.header('Health Intake Questionnaire', divider='rainbow')
st.markdown('''Welcome To! :blue[O] :blue[S] :blue[T] :blue[F] - :blue[Organization]''')
# code = '''print("Made by: Hassan Mustafa")'''
# st.code(code, language='python')


tab1, tab2 = st.tabs(["Q & A", "Stored Data"])

with tab1:
    ask_question()

with tab2:
        st.write("### User Stored Data")
        for i, (question, _) in enumerate(questions):
            response_key = f"response_{i}"
            if response_key in st.session_state.responses:
                st.write(f"Q{i+1} - {question} <br> A{i+1} - {st.session_state.responses[response_key]}", unsafe_allow_html=True)

