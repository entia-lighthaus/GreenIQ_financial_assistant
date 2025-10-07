# test_installation.py
try:
    import google.generativeai as genai
    print("google-generativeai - OK")
except ImportError as e:
    print(f" google-generativeai - FAILED: {e}")

try:
    import streamlit
    print("streamlit - OK")
except ImportError as e:
    print(f" streamlit - FAILED: {e}")

try:
    import speech_recognition
    print("speechrecognition - OK")
except ImportError as e:
    print(f" speechrecognition - FAILED: {e}")

try:
    import pygame
    print("pygame - OK")
except ImportError as e:
    print(f" pygame - FAILED: {e}")

try:
    from dotenv import load_dotenv
    print("python-dotenv - OK")
except ImportError as e:
    print(f" python-dotenv - FAILED: {e}")

try:
    from gtts import gTTS
    print("gtts - OK")
except ImportError as e:
    print(f" gtts - FAILED: {e}")

try:
    import pytesseract
    print("pytesseract - OK")
except ImportError as e:
    print(f"pytesseract - FAILED: {e}")

try:
    from PIL import Image
    print("pillow - OK")
except ImportError as e:
    print(f"pillow - FAILED: {e}")

print("\n Installation check complete!")