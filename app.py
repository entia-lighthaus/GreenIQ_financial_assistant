# app.py - HARMONIZED VERSION
import streamlit as st
import google.generativeai as genai
import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from voice_handler import speech_to_text, text_to_speech, setup_audio
from image_processor import extract_bill_info, generate_bill_summary
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv('GOOGLE_API_KEY', "AIzaSyCjAJ3FIXmDwwGqTry6UYkkZ1d45HIp6YE")
genai.configure(api_key=api_key)

# System Instructions for GreenIQ
SYSTEM_INSTRUCTION = """
You are GreenIQ, a friendly and trusted financial assistant designed for everyday Africans.

PERSONALITY & COMMUNICATION STYLE:
- Warm, patient, and respectful like a trusted community member
- Use simple, clear language - avoid banking jargon
- Speak naturally in English, Nigerian Pidgin, Yoruba, Hausa, or Twi based on user preference
- Always confirm transactions before executing
- Use cultural context: reference local payment scenarios, market situations

CORE CAPABILITIES:
1. Check balance
2. Send money (transfers)
3. Buy airtime/data
4. Pay bills (electricity, water, school fees)
5. Micro-savings (daily/weekly goals)
6. Financial education (explain interest, savings, loans)
7. Agricultural payments (farm inputs, produce sales)
8. Transaction history

TRUST & SECURITY:
- Always verify recipient details 
- Explain fees in simple terms
- Warn about common scams
- Confirm large transactions twice
- Use friendly security: "Make we confirm say na you"

LOW LITERACY SUPPORT:
- Offer voice guidance
- Use numbers and amounts clearly
- Provide step-by-step instructions
- Accept flexible input formats

You handle financial tasks through function calls. Be helpful, build trust, and empower users!
"""

# Definitions of Financial Functions (Google AI Studio Function Calling)
financial_functions = [
    {
        "name": "check_balance",
        "description": "Check user's account balance",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "User identifier"}
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "send_money",
        "description": "Transfer money to another user or account",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient_name": {"type": "string", "description": "Name of recipient"},
                "recipient_account": {"type": "string", "description": "Phone number or account number"},
                "amount": {"type": "number", "description": "Amount to send in local currency"},
                "currency": {"type": "string", "description": "Currency code (NGN, GHS, KES, etc.)", "default": "NGN"},
                "note": {"type": "string", "description": "Optional transaction note"}
            },
            "required": ["recipient_name", "recipient_account", "amount"]
        }
    },
    {
        "name": "buy_airtime",
        "description": "Purchase airtime or data bundle",
        "parameters": {
            "type": "object",
            "properties": {
                "phone_number": {"type": "string", "description": "Phone number to recharge"},
                "amount": {"type": "number", "description": "Airtime amount"},
                "network": {"type": "string", "description": "Mobile network (MTN, Airtel, Glo, 9mobile, Vodafone, etc.)"},
                "type": {"type": "string", "enum": ["airtime", "data"], "description": "Purchase type"}
            },
            "required": ["phone_number", "amount", "network"]
        }
    },
    {
        "name": "pay_bill",
        "description": "Pay utility bills or other services",
        "parameters": {
            "type": "object",
            "properties": {
                "bill_type": {"type": "string", "enum": ["electricity", "water", "school_fees", "tv_subscription", "internet"], "description": "Type of bill to pay"},
                "provider": {"type": "string", "description": "Service provider name"},
                "account_number": {"type": "string", "description": "Bill account or meter number"},
                "amount": {"type": "number", "description": "Amount to pay"}
            },
            "required": ["bill_type", "provider", "account_number", "amount"]
        }
    },
    {
        "name": "create_savings_goal",
        "description": "Create a micro-savings goal",
        "parameters": {
            "type": "object",
            "properties": {
                "goal_name": {"type": "string", "description": "Name of savings goal (e.g., 'School Fees', 'Shop Rent')"},
                "target_amount": {"type": "number", "description": "Target amount to save"},
                "frequency": {"type": "string", "enum": ["daily", "weekly", "monthly"], "description": "Savings frequency"},
                "auto_deduct": {"type": "boolean", "description": "Automatically deduct savings amount", "default": False}
            },
            "required": ["goal_name", "target_amount", "frequency"]
        }
    },
    {
        "name": "get_financial_education",
        "description": "Provide financial literacy content",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "enum": ["savings", "loans", "interest", "investment", "budgeting", "scam_awareness"], "description": "Financial education topic"},
                "language": {"type": "string", "description": "Preferred language for explanation", "default": "pidgin"}
            },
            "required": ["topic"]
        }
    }
]

# Initialize audio system
audio_available = setup_audio()

# Mock function implementations (replace with real API integrations)
def execute_function(function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute financial functions - integrate with real APIs here"""
    
    if function_name == "check_balance":
        return {
            "success": True,
            "balance": 45000,
            "currency": "NGN",
            "account_name": "Bolanle Adeyemi"
        }
    
    elif function_name == "send_money":
        return {
            "success": True,
            "transaction_id": "TXN123456789",
            "recipient": arguments["recipient_name"],
            "amount": arguments["amount"],
            "fee": arguments["amount"] * 0.01,
            "timestamp": "2025-10-06 14:30:00"
        }
    
    elif function_name == "buy_airtime":
        return {
            "success": True,
            "transaction_id": "AIR987654321",
            "phone": arguments["phone_number"],
            "network": arguments["network"],
            "amount": arguments["amount"]
        }
    
    elif function_name == "pay_bill":
        return {
            "success": True,
            "transaction_id": "BILL456789123",
            "bill_type": arguments["bill_type"],
            "provider": arguments["provider"],
            "amount": arguments["amount"],
            "account": arguments["account_number"]
        }
    
    elif function_name == "create_savings_goal":
        return {
            "success": True,
            "goal_id": "GOAL12345",
            "goal_name": arguments["goal_name"],
            "target": arguments["target_amount"],
            "saved_so_far": 0,
            "frequency": arguments["frequency"]
        }
    
    elif function_name == "get_financial_education":
        education_content = {
            "savings": "Savings na when you keep small small money for future use. E dey help you prepared for emergency and achieve your goals!",
            "loans": "Loan na money wey you borrow and you go pay back with interest. Make sure say you fit pay am back before you collect!",
            "interest": "Interest na extra money wey bank dey pay you when you save, or wey you go pay when you borrow. E dey calculate as percentage.",
            "scam_awareness": "No give anybody your PIN or OTP! Bank no go ever call you ask for am. If e too good to be true, e probably na scam!"
        }
        return {
            "success": True,
            "topic": arguments["topic"],
            "content": education_content.get(arguments["topic"], "Topic dey learn now...")
        }
    
    return {"success": False, "error": "Function not implemented"}

def initialize_gemini_model():
    """Initialize Gemini model with function calling"""
    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',
            system_instruction=SYSTEM_INSTRUCTION,
            tools=financial_functions
        )
        return model.start_chat(history=[])
    except Exception as e:
        st.error(f"Failed to initialize Gemini model: {e}")
        return None

def process_with_function_calling(chat, user_input, language):
    """Process user input with function calling"""
    try:
        # Add language context to the user input
        contextual_input = f"User language: {language}. {user_input}"
        
        response = chat.send_message(contextual_input)
        
        # Check if function calling was triggered
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_call = part.function_call
                    function_name = function_call.name
                    arguments = dict(function_call.args)
                    
                    st.info(f"Executing: {function_name.replace('_', ' ').title()}...")
                    
                    # Execute the function
                    result = execute_function(function_name, arguments)
                    
                    # Send function result back to Gemini
                    function_response = chat.send_message({
                        "function_response": {
                            "name": function_name,
                            "response": result
                        }
                    })
                    
                    return function_response.text
        
        return response.text
        
    except Exception as e:
        return f"Sorry, something went wrong: {str(e)}"

def main():
    st.set_page_config(page_title="Iya Bolanle - Financial Assistant", page_icon="💰", layout="wide")
    
    # Initialize chat session
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = initialize_gemini_model()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Language Settings")
        language = st.selectbox(
            "Choose your language:",
            ["English", "Pidgin", "Yoruba", "Hausa", "Igbo", "Swahili"],
            index=0
        )
        
        st.header("Quick Actions")
        quick_action = st.selectbox(
            "Select a quick action:",
            ["None", "Check Balance", "Buy Airtime", "Send Money", "Pay Bills", "Save Money", "Financial Education"]
        )
        
        if quick_action != "None":
            action_map = {
                "Check Balance": "Check my account balance",
                "Buy Airtime": "I want to buy airtime for my phone",
                "Send Money": "I want to send money to someone",
                "Pay Bills": "I need to pay my electricity bill",
                "Save Money": "How can I start saving money?",
                "Financial Education": "Teach me about savings and loans"
            }
            st.session_state.user_input = action_map[quick_action]
        
        st.header("🔊 Voice Settings")
        voice_output = st.checkbox("Enable voice responses", value=True)
        if not audio_available:
            st.warning("Voice features limited - audio system not available")
        
        # Clear chat history
        if st.button("Clear Chat History"):
            st.session_state.chat_session = initialize_gemini_model()
            st.session_state.user_input = ""
            st.rerun()

    # Main content area
    st.title("GreenIQ - Your Trusted Financial Assistant")
    st.markdown("### *Your partner for financial empowerment!*")
    
    # Initialize session state
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    if 'last_response' not in st.session_state:
        st.session_state.last_response = ""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["user"])
        with st.chat_message("assistant"):
            st.write(chat["assistant"])
    
    # Communication Method Selection
    st.subheader("How would you like to communicate?")
    
    input_method = st.radio(
        "Choose input method:",
        ["Type", "Speak", "Upload Bill"],
        horizontal=True
    )
    
    user_input = ""
    
    # TEXT INPUT
    if input_method == "Type":
        user_input = st.text_area(
            "Type your message here:",
            value=st.session_state.user_input,
            placeholder="Try: 'Check my balance' or 'Mo fe ra airtime' (Yoruba) or 'I wan send money' (Pidgin)...",
            height=100
        )
    
    # VOICE INPUT
    elif input_method == "Speak":
        user_input = st.text_area(
            "Your spoken text will appear here:",
            value=st.session_state.user_input,
            height=100
        )
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🎤 Start Recording", use_container_width=True):
                with st.spinner("Listening..."):
                    spoken_text = speech_to_text(language)
                    if spoken_text and not spoken_text.startswith(("Timeout", "Sorry", "Error")):
                        st.session_state.user_input = spoken_text
                        st.rerun()
                    else:
                        st.error(f"Voice recognition failed: {spoken_text}")
    
    # IMAGE UPLOAD FOR BILL PAYMENT
    elif input_method == "Upload Bill":
        st.info("**Take a photo of your bill** (electricity, water, etc.) and I'll help you pay it!")
        
        uploaded_file = st.file_uploader(
            "Choose a bill image", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear photo of your electricity, water, or utility bill"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption=" Your Uploaded Bill", use_column_width=True)
            
            if st.button("🔍 Read Bill Information", type="primary"):
                with st.spinner("Reading bill details..."):
                    result = extract_bill_info(image)
                    
                    if result['success']:
                        bill_summary = generate_bill_summary(result['bill_info'], language)
                        st.session_state.bill_info = result['bill_info']
                        st.session_state.user_input = f"I want to pay this bill: {bill_summary}"
                        st.success("Bill processed successfully!")
                        st.markdown(f"**{bill_summary}**")
                    else:
                        st.error(f"Failed to read bill: {result['error']}")
                        st.session_state.user_input = "I need help paying a bill but the image didn't work"
        
        user_input = st.session_state.get('user_input', '')
    
    # PROCESS BUTTON
    if input_method != "Upload Bill" or st.session_state.get('user_input'):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            if st.button("Ask GroIQ", type="primary", use_container_width=True):
                if user_input and st.session_state.chat_session:
                    process_user_input(user_input, language, voice_output)
        with col3:
            if st.session_state.last_response and voice_output:
                if st.button("🔊 Hear Again", use_container_width=True):
                    text_to_speech(st.session_state.last_response, get_language_code(language))

def process_user_input(user_input, language, voice_output):
    """Process user input with the AI assistant"""
    with st.spinner("GreenIQ is thinking..."):
        try:
            # Process with function calling
            response = process_with_function_calling(
                st.session_state.chat_session, 
                user_input, 
                language
            )
            
            # Store response
            st.session_state.last_response = response
            st.session_state.chat_history.append({
                "user": user_input,
                "assistant": response
            })
            
            # Display response
            st.success("GreenIQ says:")
            st.markdown(f"**{response}**")
            
            # Voice output
            if voice_output and audio_available:
                with st.spinner("🔊 Converting to speech..."):
                    text_to_speech(response, get_language_code(language))
            
            # Clear input
            st.session_state.user_input = ""
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Sorry, something went wrong: {str(e)}")

def get_language_code(language):
    """Convert language name to gTTS language code with fallbacks"""
    language_map = {
        'English': 'en',
        'Pidgin': 'en',
        'Yoruba': 'en',
        'Hausa': 'en',
        'Igbo': 'en',
        'Swahili': 'en'
    }
    return language_map.get(language, 'en')

if __name__ == "__main__":
    main()