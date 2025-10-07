# image_processor.py (Simplified - No OpenCV required)
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import streamlit as st
import re

def extract_bill_info(image):
    """
    Extract bill information from uploaded image using OCR
    Returns: dictionary with bill details
    """
    try:
        # Preprocess image using PIL only (no OpenCV)
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
        
        # Apply slight blur to reduce noise
        image = image.filter(ImageFilter.MedianFilter(size=3))
        
        # Perform OCR
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        
        # Extract bill information
        bill_info = analyze_bill_text(text)
        
        return {
            'success': True,
            'raw_text': text,
            'bill_info': bill_info,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'raw_text': '',
            'bill_info': {},
            'error': str(e)
        }

def analyze_bill_text(text):
    """
    Analyze OCR text to extract bill details
    """
    bill_info = {}
    
    # Common bill patterns
    patterns = {
        'amount_due': [
            r'(?:amount due|balance due|total due|payment due)[:\s]*[\$₦]?\s*([0-9,]+\.?[0-9]*)',
            r'(?:total|amount)[:\s]*[\$₦]?\s*([0-9,]+\.?[0-9]*)',
            r'[\$₦]\s*([0-9,]+\.?[0-9]*)'
        ],
        'account_number': [
            r'(?:account|acct|customer)[\s#:]*([A-Z0-9\-]+)',
            r'account number[\s:]*([A-Z0-9\-]+)'
        ],
        'due_date': [
            r'(?:due date|payment due)[:\s]*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})',
            r'(?:due date|payment due)[:\s]*([A-Za-z]+\s+[0-9]{1,2},\s+[0-9]{4})'
        ],
        'company': [
            r'(IKEDC|Eko Electric|PHED|IBEDC|AEDC|KEDCO|BEDC)',
            r'(Lagos|Abuja|Port Harcourt|Ibadan|Kano|Kaduna).*?(Electric|Water|Utility)'
        ]
    }
    
    for field, regex_list in patterns.items():
        for pattern in regex_list:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                bill_info[field] = matches[0]
                break
    
    return bill_info

def generate_bill_summary(bill_info, language='English'):
    """
    Generate a user-friendly summary of the bill
    """
    if not bill_info:
        return "I couldn't find clear bill information in the image. Please try a clearer photo or enter the details manually."
    
    summary_parts = []
    
    # Company
    if bill_info.get('company'):
        summary_parts.append(f"**Company:** {bill_info['company']}")
    
    # Amount
    if bill_info.get('amount_due'):
        amount = bill_info['amount_due']
        summary_parts.append(f"**Amount Due:** ₦{amount}")
    
    # Account Number
    if bill_info.get('account_number'):
        summary_parts.append(f"**Account:** {bill_info['account_number']}")
    
    # Due Date
    if bill_info.get('due_date'):
        summary_parts.append(f"**Due Date:** {bill_info['due_date']}")
    
    if not summary_parts:
        return "I found some text but couldn't identify bill details. Please check if the bill is clear and try again."
    
    summary = "I found these bill details:\n\n" + "\n".join(summary_parts)
    
    # Add language-specific instructions
    if language != 'English':
        language_notes = {
            'Yoruba': "\n\nṢe o fẹ tẹsiwaju pẹlu iṣanwo?",
            'Pidgin': "\n\nYou wan continue with payment?",
            'Hausa': "\n\nKuna son ci gaba da biyan?",
            'Igbo': "\n\nỊ chọrọ ịga n'ihu na ịkwụ ụgwọ?",
            'Swahili': "\n\nUnataka kuendelea na malipo?"
        }
        summary += language_notes.get(language, "\n\nDo you want to proceed with payment?")
    else:
        summary += "\n\nDo you want to proceed with payment?"
    
    return summary