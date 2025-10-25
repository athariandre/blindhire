#!/bin/bash

# Test runner script for BlindHire ML Microservice
set -e

echo "🧪 Running BlindHire ML Microservice Test Suite"
echo "================================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: No virtual environment detected"
    echo "   Consider activating a virtual environment first"
fi

# Set test environment variables
export ML_USE_FALLBACK=true
export GEMINI_API_KEY=""

# Install test dependencies if not already installed
echo "📦 Installing test dependencies..."
pip install -q pytest pytest-asyncio httpx

# Run the tests
echo "🚀 Running tests..."
pytest tests/ -v

echo ""
echo "✅ Test suite completed!"
echo ""
echo "📊 Test Coverage Summary:"
echo "========================="
echo "- FastAPI endpoints: Health, Parse & Score, Explain Terms"
echo "- Resume anonymization (regex fallback & Gemini)"
echo "- Text vectorization (TF-IDF fallback & SentenceTransformers)" 
echo "- Hash computation and integrity"
echo "- Configuration management"
echo "- Error handling and edge cases"
echo "- Integration testing"
echo ""
echo "🔧 To run specific test categories:"
echo "   pytest tests/test_app.py -v              # API tests"
echo "   pytest tests/test_parser.py -v           # Parser tests"
echo "   pytest tests/test_vectorizer.py -v       # Vectorizer tests"
echo "   pytest tests/test_hashing.py -v          # Hashing tests"
echo "   pytest tests/test_config.py -v           # Config tests"