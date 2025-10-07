import google.generativeai as genai

genai.configure(api_key="AIzaSyCjAJ3FIXmDwwGqTry6UYkkZ1d45HIp6YE")

print("🔍 Checking available models...")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ Available: {model.name}")