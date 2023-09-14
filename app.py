import os
import requests
import json

import streamlit as st
from streamlit_lottie import st_lottie

import audio_recorder
import tts_converter
import whisper
import chat_ai


LOTTIE_URL = 'https://assets6.lottiefiles.com/packages/lf20_6e0qqtpa.json'
PROMPT_WAVFILE = 'prompt.wav'

# lottie animation file for the floating robot
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return
    return r.json()

lottie_anim = load_lottie(LOTTIE_URL)

st.set_page_config(page_title="ChatGPT-VA", page_icon='', layout='centered')


if "is_recording" not in st.session_state:
    st.session_state.is_recording = False
if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = None
if "chat_text" not in st.session_state:
    st.session_state.chat_text = None


def callback_record():
    st.session_state.is_recording = True
    prompt_box.write("Listening ...")

    audio_recorder.record(filename=PROMPT_WAVFILE)
    prompt_box.write("Processing the question ...")


    prompt = whisper.get_transcription(PROMPT_WAVFILE)

    st.session_state.is_recording = False
    st.session_state.prompt_text = prompt

    response = chat_ai.get_response(prompt)
    print(response)
    json.dump(response, open('response.json', 'wt'))

    st.session_state.chat_text = response



with st.container():
    left, right = st.columns([2, 3])
    with left:
        st_lottie(lottie_anim, height=300, key='coding')

    with right:
        st.subheader('Hi, I am Eduskills OET Voice Assistant!')

        st.write('Press speak to start recording your voice')

        rec_button = st.button(
            label="Speak :microphone:", type='primary',
            on_click=callback_record,
            disabled=st.session_state.is_recording)

        prompt_box = st.empty()
        if st.session_state.prompt_text:
            prompt_box.write(f'Prompt: {st.session_state.prompt_text}')



with st.container():
    st.write('---')

    message_box = st.empty()
    if st.session_state.chat_text:
        choice = st.session_state.chat_text['choices'][0]
        for line in choice['message']['content'].split('\n'):
            if not line:
                continue
            message_box.write(line)
            tts_converter.run_tts(line)

        message_box.write(choice['message']['content'])