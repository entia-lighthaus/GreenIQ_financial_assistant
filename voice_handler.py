# voice_handler.py
import speech_recognition as sr
import streamlit as st
from gtts import gTTS
import io
import pygame
import time

def setup_audio():
    """Initialize pygame mixer for audio playback"""
    try:
        pygame.mixer.init()
        return True
    except:
        return False

def text_to_speech(text, language='en'):
    """Convert text to speech and play it with language fallback"""
    try:
        # For African languages, fallback to English TTS but keep the text response
        supported_languages = ['en', 'fr', 'es', 'de', 'it', 'pt']  # gTTS supported languages
        
        # If language not supported, use English but mention it
        if language not in supported_languages:
            # Add a prefix in English explaining we'll read in English
            english_prefix = "Here's your response in English: "
            full_text = english_prefix + text
            tts_language = 'en'
        else:
            full_text = text
            tts_language = language
        
        tts = gTTS(text=full_text, lang=tts_language, slow=False)
        
        # Save to bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Play audio
        pygame.mixer.music.load(audio_buffer)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        return True
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return False

def speech_to_text(language='en'):
    """Convert speech to text using microphone"""
    recognizer = sr.Recognizer()
    
    # Map languages to speech recognition languages
    language_map = {
        'English': 'en-US',
        'Pidgin': 'en-US',  # Pidgin will use English recognition
        'Yoruba': 'en-US',  # Fallback to English recognition for Yoruba
        'Hausa': 'en-US',   # Fallback to English recognition for Hausa
        'Igbo': 'en-US',    # Fallback to English recognition for Igbo
        'Swahili': 'en-US'  # Fallback to English recognition for Swahili
    }
    
    sr_language = language_map.get(language, 'en-US')
    
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10)
            
        st.info(" Processing your speech...")
        text = recognizer.recognize_google(audio, language=sr_language)
        return text
        
    except sr.WaitTimeoutError:
        return "Timeout: No speech detected"
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio"
    except sr.RequestError as e:
        return f"Error with speech recognition service: {e}"
    except Exception as e:
        return f"Microphone error: {e}"