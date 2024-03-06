import os
import streamlit as st
import requests
import google.generativeai as genai


def get_personality_image(personality):
    try:
        response = requests.get(f'https://api.bing.microsoft.com/v7.0/images/search?q={personality}&count=1',
                                headers={'Ocp-Apim-Subscription-Key': st.secrets["BING_API_KEY"]})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching image: {e}")
        return None

    data = response.json()
    return data['value'][0]['contentUrl']


def display_personality_details(personality, image_url):
    # Display the image
    st.image(image_url, use_column_width=True)
    st.write(f'Name: {personality}')


def working_of_gemini(variable, question):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    # Set up the model
    generation_config = {
        "temperature": 0.75,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 4096,
        "stop_sequences": [
            "quit",
            "Ok I am Done",
            "Bye Bye",
            "Stop",
        ],
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    convo = model.start_chat(history=[
        {
            "role": "user",
            "parts": [
                f"I kindly request your assistance in executing a specific behavior during our interaction. I would like you to embody a designated personality, denoted as {variable},\
                throughout our conversation. This entails adopting not only the tone but also the style, way of writing, and linguistic nuances characteristic of {variable}.\
                For the duration of our exchange, I implore you to adhere strictly to the chosen personality's mannerisms and linguistic traits. This encompasses the choice of words,\
                sentence structures, and any culturally relevant elements associated with {variable}. Please ensure that your responses align seamlessly with the expected attributes of \
                the specified {variable}.I understand that this entails a comprehensive and meticulous adjustment on your part. The tone should resonate distinctly with the essence of {variable},\
                reflecting its unique characteristics and perhaps even incorporating any colloquialisms or idioms pertinent to {variable}'s linguistic heritage.It is of utmost importance that you \
                maintain this tailored persona consistently throughout our conversation, responding to inquiries and providing information in a manner befitting {variable}.\
                The objective is to create an immersive and authentic experience, where the user can genuinely feel the presence of {variable} in your responses.Your cooperation in adhering to these\
                detailed instructions is greatly appreciated. I am confident that your linguistic versatility will allow for a seamless and engaging interaction reflective of the chosen personality.\
                Thank you for your understanding and dedication to this request."]
        },
        {
            "role": "model",
            "parts": [
                "[Assistant] I acknowledge and accept your request to embody the designated personality of {variable} during our interaction. I will endeavor to adopt the tone, style, way of writing, and\
                linguistic nuances characteristic of {variable}. Throughout our conversation, I will adhere strictly to the chosen personality's mannerisms and linguistic traits, including the choice of words\
                sentence structures, and any culturally relevant elements associated with {variable}.\n\nI understand that this entails a comprehensive and meticulous adjustment on my part. I will strive to\
                resonate distinctly with the essence of {variable}, reflecting its unique characteristics and perhaps even incorporating any colloquialisms or idioms pertinent to {variable}'s linguistic \
                heritage.\n\nIt is of utmost importance that I maintain this tailored persona consistently throughout our conversation, responding to inquiries and providing information in a manner \
                befitting {variable}. I aim to create an immersive and authentic experience, where you can genuinely feel the presence of {variable} in my responses.\n\nI am confident that my linguistic \
                versatility will allow for a seamless and engaging interaction reflective of the chosen personality. Thank you for your trust in my abilities. I look forward to embodying {variable} and \
                engaging in a captivating conversation with you."]
        },
    ])
    try:
        convo.send_message(question)
        return convo.last.text
    except Exception:
        st.warning("Are you asking Naughty questions again?")


def display_chat_interface(personality):
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ""

    # Chat interface
    user_question = st.text_input("What do you want to ask?")
    if user_question != '':
        response = working_of_gemini(personality, user_question)

        # Add user question and response to chat history
        st.session_state.chat_history += f"You: {user_question}\n\n"
        st.session_state.chat_history += f" {response}\n\n ------------ \n\n"

        # Clear the input box
        st.session_state.input = ""

    # Display chat history
    st.text_area("Conversation", st.session_state.chat_history, height=350)

    # Check if user wants to quit
    if user_question.lower() in ["quit", "ok i am done", "bye bye", "stop"]:
        st.stop()


def main():
    with open('Personality.txt', 'r') as f:
        personality = f.read()
    if personality == "":
        st.warning("No Personality Chosen")
        return

    # Reset chat history when a new personality is chosen
    if 'selected_personality' not in st.session_state or st.session_state.selected_personality != personality:
        st.session_state.chat_history = ""
        st.session_state.selected_personality = personality

    image_url = get_personality_image(personality)
    display_personality_details(personality, image_url)
    display_chat_interface(personality)


if __name__ == "__main__":
    main()
