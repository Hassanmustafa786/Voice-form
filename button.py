import streamlit as st
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if 'but_a' not in st.session_state:
    st.session_state.disabled = False

print('before:', st.session_state)

button_a = st.button('a', key='but_a')

button_b = st.button('b', key='but_b')

# change state before creating button `c` (but after creating button `a` and `b`)

if button_a:
    st.session_state.disabled = True

if button_b:
    st.session_state.disabled = True

button_c = st.button('c', key='but_c', disabled=st.session_state.disabled)

st.write(button_a, button_b, button_c)

# display text after displaying all buttons

if button_a:
    st.write("clicked A - Activate C")
    speak("Button A")

if button_b:
    st.write("clicked B - Deactivate C")
    speak("Button B")

print('after:', st.session_state)