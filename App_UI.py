import streamlit as st

# Handle all potentially problematic imports
try:
    import speech_recognition as sr
    SPEECH_ENABLED = True
except ImportError:
    SPEECH_ENABLED = False
    st.warning("Speech recognition is not available in the cloud deployment.")

try:
    from pygame import mixer
    AUDIO_ENABLED = True
except ImportError:
    AUDIO_ENABLED = False
    st.warning("Audio playback is not available in the cloud deployment.")

try:
    from gtts import gTTS
    GTTS_ENABLED = True
except ImportError:
    GTTS_ENABLED = False
    st.warning("Text-to-speech is not available in the cloud deployment.")

# Add checks before using any of these features
def text_to_speech(text):
    if not GTTS_ENABLED:
        st.error("Text-to-speech is not available in this environment.")
        return
    # Your gTTS code here

def speech_to_text():
    if not SPEECH_ENABLED:
        st.error("Speech recognition is not available in this environment.")
        return
    # Your speech recognition code here

def play_audio():
    if not AUDIO_ENABLED:
        st.error("Audio playback is not available in this environment.")
        return
    # Your audio playback code here
