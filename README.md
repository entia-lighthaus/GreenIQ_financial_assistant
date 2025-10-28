GreenIQ - Financial Assistant 

# Project Overview
GreenIQ is an AI-powered financial assistant designed to promote financial inclusion for underserved communities across Africa. The assistant enables users to perform essential banking tasks through natural voice and text conversations in multiple African languages.


# CORE FEATURES COMPLETED

1. AI-Powered Multilingual Assistant

- - Google Gemini 2.0 Flash Integration with function calling

- - 6 Language Support: English, Pidgin, Yoruba, Hausa, Igbo, Swahili

- - Cultural Context: Responses tailored to African financial scenarios

- - GreenIQ Personality: Warm, patient, and trustworthy assistant persona


2. Voice-First Interface

- - Speech-to-Text: Voice input using Google Speech Recognition

- - Text-to-Speech: Voice responses with gTTS (Google Text-to-Speech)

- - Language Fallbacks: Smart handling of unsupported language TTS


3. Financial Operations Framework

Function Calling Architecture for real financial operations:
- - check_balance - Account balance inquiry
- - send_money - Money transfers to contacts
- - buy_airtime - Airtime and data purchases
- - pay_bill - Utility bill payments
- - create_savings_goal - Micro-savings setup
- - get_financial_education - Financial literacy content


4. Image Processing for Bills
- OCR Integration: Tesseract-based bill reading

- Smart Parsing: Extracts amount, account number, due dates

- Bill Type Detection: Electricity, water, and utility bills


5. Streamlit Web Interface
Responsive Design: Works on mobile and desktop

- Multiple Input Methods: Text, Voice, Image upload

- Session Management: Chat history and context preservation


# TECH STACK

Frontend: Streamlit
AI Engine: Google Gemini API 2.0 Flash
Voice: SpeechRecognition + gTTS + Pygame
OCR: Tesseract + PIL (OpenCV alternative)
APIs: Ready for Paystack/Flutterwave integration


# FILE STRUCTURE

financial-assistant/
├── app.py                    # MAIN APPLICATION
├── voice_handler.py          # Voice input/output system
├── image_processor.py        # Bill OCR processing
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
└── README.md                 # This file



# KEY CODE COMPONENTS

1. Main Application (app.py)
- Complete Streamlit interface with sidebar configuration

- Multilingual chat session management

- Function calling integration with Gemini

- Voice and image input handling


2. Voice Handler (voice_handler.py)

def speech_to_text(language):  # Converts speech to text
def text_to_speech(text, language):  # Converts text to speech
def setup_audio():  # Initializes audio system


# CURRENT CAPABILITIES

Working Financial Operations

- Balance Inquiry: "Check my balance" / "Mo fe ri iye owo mi"

- Money Transfer: "Send 5000 naira to Tunde"

- Airtime Purchase: "Buy 1000 naira MTN airtime"

- Bill Payments: "Pay my electricity bill"

- Savings Goals: "I want to save for school fees"

- Financial Education: "Teach me about interest"


Multilingual Examples

- English: "How do I transfer money?"

- Pidgin: "How I fit send money give my brother?"

- Yoruba: "Bawo ni mo se le ran owo si ile-iwe?"

- Hausa: "Yaya zan iya aika kudi?"

- Responses maintain cultural context and simplicity


# USER EXPERIENCE FEATURES
- Voice Confirmation: "You want send 5000 naira to Tunde, abi?"

- Step-by-Step Guidance: Clear instructions for each operation

- Error Handling: Graceful failure with helpful suggestions

- Session Memory: Remembers conversation context


# TO RUN THE APPLICATION

Run the command in terminal: 

- streamlit run app.py


# TEST THE SYSTEM

- Open http://localhost:8501 in browser

- Select preferred language

- Try voice commands or type requests

- Test bill upload with sample images


# KEY FEATURES TO SHOWCASE

- Natural multilingual conversations

- Voice-first interface

- Real financial operations

- Bill image processing

- Cultural context awareness


#  NEXT STEPS & OPPORTUNITIES

Immediate Enhancements
- Payment API Integration - Connect to real banking APIs

- UI/UX Polish - Better mobile experience

- Advanced Error Handling - Network failure scenarios

- User Testing - Validate with target user personas


# FUTURE EXPANSION

USSD Fallback for poor network areas

WhatsApp Integration for wider reach

Advanced Security - Voiceprint authentication

Community Features - Group savings (Ajo/Esusu)
