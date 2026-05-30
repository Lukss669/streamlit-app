from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import streamlit as st
from gtts import gTTS
import io

import streamlit as st

st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1542751371-adc38448a05e");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)

tab_1, tab_2, tab_3 = st.tabs(
    ["Chat", "Playback Bar", "History"]
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("my_keyy"),
    base_url="https://api.groq.com/openai/v1"
)

with open("games.json", "r") as file:
    prompts = json.load(file)

with open("style.json", "r") as file:
    prompts1 = json.load(file)

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = ""

if "system_prompt1" not in st.session_state:
    st.session_state.system_prompt1 = ""

if "response_text" not in st.session_state:
    st.session_state.response_text = ""

if "history" not in st.session_state:
    with open("historyyyy.json", "r") as file:
        st.session_state.history = json.load(file)

with tab_1:

    st.header("Gaming Assistant")

    user_input = st.text_input("Enter question:")

    answer_style = st.sidebar.selectbox(
        "Select Answer Style:",
        [
            "Superficial explanation",
            "In-depth explanation",
            "Expert"
        ]
    )

    if answer_style == "Superficial explanation":
        st.session_state.system_prompt1 = prompts1["Superficial explanation"]

    elif answer_style == "In-depth explanation":
        st.session_state.system_prompt1 = prompts1["In-depth explanation"]

    elif answer_style == "Expert":
        st.session_state.system_prompt1 = prompts1["Expert"]

    subject = st.sidebar.selectbox(
        "Select Category:",
        [
            "Brawl Stars",
            "Pubg mobile",
            "Minecraft",
            "CSGO",
            "CarParking",
        ]
    )

    if subject == "Brawl Stars":
        st.session_state.system_prompt = prompts["brawlstars"]

    elif subject == "Pubg mobile":
        st.session_state.system_prompt = prompts["pubgmobile"]

    elif subject == "Minecraft":
        st.session_state.system_prompt = prompts["minecraft"]

    elif subject == "CSGO":
        st.session_state.system_prompt = prompts["csgo"]

    elif subject == "CarParking":
        st.session_state.system_prompt = prompts["carparking"]

    ai_role = [
        {
            "role": "system",
            "content": st.session_state.system_prompt
        }
    ]

    ai_textstyle = [
        {
            "role": "system",
            "content": st.session_state.system_prompt1
        }
    ]

    if st.button("Send"):

        st.session_state.history.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        full_message = ai_role + ai_textstyle + st.session_state.history
        

        response = client.responses.create(
            model="openai/gpt-oss-20b",
            input=full_message
        )

        st.session_state.response_text = response.output_text

        st.session_state.history.append(
            {
                "role": "assistant",
                "content": response.output_text
            }
        )
        
        st.session_state.history = st.session_state.history

        with open("historyyyy.json", "w") as file:
            json.dump(st.session_state.history, file, indent=4)

        

with tab_2:

    st.header("Audio Playback")

    if st.session_state.response_text != "":

        tts = gTTS(
            text=st.session_state.response_text,
            lang="en"
        )

        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        st.audio(
            audio_bytes,
            format="audio/mp3",
            autoplay=True
        )


with tab_3:

    st.header("Chat History")

    for message in st.session_state.history:
        st.write(f"{message["role"]}, {message["content"]}")



    
