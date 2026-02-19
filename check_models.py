"""
Check what Gemini models are available with the API key
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Using API key: {api_key[:20]}...")

genai.configure(api_key=api_key)

print("\n" + "="*60)
print("Available Gemini Models:")
print("="*60)

try:
    models = genai.list_models()
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"\n✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description[:80]}...")
except Exception as e:
    print(f"❌ Error listing models: {e}")

print("\n" + "="*60)
