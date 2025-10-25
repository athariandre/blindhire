#!/usr/bin/env python3
import google.generativeai as genai
from config import get_gemini_api_key

try:
    genai.configure(api_key=get_gemini_api_key())
    print("Available Gemini models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  {m.name}")
except Exception as e:
    print(f"Error: {e}")