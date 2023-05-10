import requests
import streamlit as st
import pyaudio
import wave
import openai
import os
import googletrans
import time
import vlc

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "input.wav"

# Define OpenAI API keys.
openai.apikey = os.getenv("OPENAI_API_KEY")



# Define the language translator.
translator = googletrans.Translator()

# Use the translate function to translate the text depending on the language selected in the sidebar.
def translate(text, language):
    if language == "English":
        return translator.translate(text, dest='en').text
    else:
        return translator.translate(text, dest=language).text
    
# Select the language to translate to in the sidebar.
language = st.sidebar.selectbox("Select Language", ("English", "Punjabi"))

if language == "English":
    st.title("English A.I.")
else:
    st.title("ਪੰਜਾਬੀ ਏ.ਆਈ.")


# Define the text on the button depending on the language selected in the sidebar.
if language == "English":
    button_text = "Start Recording 🔉"
else:
    button_text = "ਰਿਕਾਰਡਿੰਗ ਸ਼ੁਰੂ ਕਰੋ 🔉"

record_button = st.button(button_text, key="record")                                                

# Record the audio when the button is pressed.

# Define the input box depending on the language selected in the sidebar.
if language == "English":
    input_text = st.text_area("Input Text", value="", height=100, max_chars=None, key=None)
else:
    input_text = st.text_area("ਇੰਪੁੱਟ ਟੈਕਸਟ", value="", height=100, max_chars=None, key=None)

# Define the text on the button depending on the language selected in the sidebar.
if language == "English":
    button_text = "Submit"
else:
    button_text = "ਜਮ੍ਹਾਂ ਕਰੋ"

submit = st.button(button_text, key="submit")

# Submit button
def submit(input_text):
    # Get user input question
    q = input_text
    
    # Send to OpenAI
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=q + "Explain like I'm 5 and be honest, truthful and elaborate. Also end at punctuation marks. Use simple vocabulary.",
    max_tokens=1000,
    temperature=0.7,
    frequency_penalty=0.2,
    top_p=0.9
    )
    
    # Get answer
    answer_text = response['choices'][0]['text']

    # Translate answer to Punjabi
    translator = googletrans.Translator()
    # translated_answer = translator.translate(answer_text, dest='pa')
    
    if language == "English":
        return answer_text
    else:
        return translate(answer_text, language)

# Define what happens when the button is pressed.
if submit:
    response = submit(input_text)
    # st.markdown(f"**Output Text:** {response.text}")
    if language == "English":
        st.text_area("Output Text", value=response, height=200, max_chars=None, key=None)
    else:
        st.text_area("ਆਉਟਪੁੱਟ ਟੈਕਸਟ", value=response, height=200, max_chars=None, key=None)
    response = response

# Define function to read out loud
def tts(response):
    # Get text from answer widget
    text = response

    apikey = 'YOUR_API_KEY'
    voice = 'Navneet'
    text = text
    url = f'https://api.narakeet.com/text-to-speech/m4a?voice={voice}'
    
    options = {
        'headers': {
            'Accept': 'application/octet-stream',
            'Content-Type': 'text/plain',
            'x-api-key': apikey,
        },
        'data': text.encode('utf8')
    }

    with open('output.mp3', 'wb') as f:
        f.write(requests.post(url, **options).content)

    # Create vlc media player object
    audio = vlc.MediaPlayer("output.mp3")

    # Start playing audio
    audio.play()

    time.sleep(10)    

# Define the text on the button depending on the language selected in the sidebar.
if language == "English":
    button_text = "Play Response 🔉"
else:
    button_text = "ਜਵਾਬ ਨੂੰ ਚਲਾਓ 🔉"

# Define a button to turn the response into audio and play it.
tts_button = st.button(button_text, key="tts")

# Define what happens when the button is pressed.
if tts_button:
    tts(response)




