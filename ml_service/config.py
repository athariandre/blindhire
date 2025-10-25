"""
Shared configuration for ML service
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Whether to use TF-IDF fallback instead of sentence transformers
# Default is False for production use
USE_FALLBACK = os.environ.get('ML_USE_FALLBACK', 'false').lower() == 'true'

# Gemini API Configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Service Configuration
ML_SERVICE_PORT = int(os.environ.get('ML_SERVICE_PORT', '8001'))
ML_SERVICE_HOST = os.environ.get('ML_SERVICE_HOST', '0.0.0.0')


def get_model_name() -> str:
    """
    Get the model name based on current configuration
    """
    if USE_FALLBACK:
        return "tfidf-fallback"
    return "all-MiniLM-L6-v2"


def get_gemini_api_key() -> str:
    """
    Get the Gemini API key from environment variables
    Raises ValueError if not set
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set. Please add it to your .env file.")
    return GEMINI_API_KEY


def validate_config():
    """
    Validate that all required configuration is present
    """
    try:
        get_gemini_api_key()
        print("✅ Gemini API key loaded successfully")
        return True
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return False
