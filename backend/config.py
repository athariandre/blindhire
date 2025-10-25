"""
Configuration for BlindHire Backend
"""
import os
from pathlib import Path

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, encoding='utf-8')
    else:
        print("⚠️  No .env file found, using default configuration")
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")
    print("   Using default configuration")

# Blockchain Configuration
SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL", "https://rpc.sepolia.org")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
FACTORY_CONTRACT_ADDRESS = os.getenv("FACTORY_CONTRACT_ADDRESS", "0x04E2AF7018Eada81e583425A4eB6Da6b1f116c7d")
CHAIN_ID = 11155111  # Sepolia

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# ML Service Configuration
ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://localhost:5000")
