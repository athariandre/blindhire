# BlindHire ML Microservice

FastAPI-based machine learning microservice for analyzing and scoring resumes against job descriptions.

## Features

- **Resume Anonymization**: Removes personally identifiable information (names, emails, phone numbers, schools)
- **Similarity Scoring**: Computes semantic similarity between resumes and job descriptions
- **Decision Classification**: Auto-pass, auto-fail, or review categories based on similarity scores
- **Deterministic Hashing**: SHA-256 hashes for resume, model, and scores for blockchain integration
- **Explanation Terms**: Extracts top terms from resumes for transparency

## Quick Start (Single Session)

All commands can be run in a single terminal session:

```bash
# Navigate to ml_service directory
cd ml_service

# Install dependencies
pip install -r requirements.txt

# Start the service (with fallback mode for testing without model download)
ML_USE_FALLBACK=true python app.py &

# Wait a few seconds for startup
sleep 5

# Test the health endpoint
curl http://127.0.0.1:8001/health

# Run quick tests
python quick_test.py

# Run comprehensive test suite
python tests/test_local.py

# Stop the service when done
pkill -f "python app.py"
```

## API Endpoints

### POST /parse_and_score
Analyzes a resume against a job description.

**Request:**
```json
{
  "resume_text": "Resume content here...",
  "job_id": "JOB-2025-001"
}
```

**Response:**
```json
{
  "similarity_score": 0.3411,
  "decision": "review",
  "resume_hash": "0x9653...",
  "model_hash": "0x07db...",
  "score_hash": "0xb2c0...",
  "explain": {
    "top_terms": ["python", "data", "science", "react", "using"]
  }
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "model": "sentence-transformers/all-MiniLM-L6-v2"
}
```

### POST /explain_terms
Extracts top terms from a resume.

**Request:**
```json
{
  "resume_text": "Resume content here..."
}
```

**Response:**
```json
{
  "top_terms": ["python", "machine", "learning", "data", "science"]
}
```

## Environment Variables

- `ML_USE_FALLBACK`: Set to `true` to use TF-IDF fallback instead of downloading the transformer model (useful for testing in restricted environments). Default is `false` (production mode with full transformer model).

## Decision Thresholds

- **auto_pass**: similarity_score >= 0.75
- **auto_fail**: similarity_score <= 0.3
- **review**: 0.3 < similarity_score < 0.75

## Testing

The service includes two test files:

1. **quick_test.py**: Fast sanity check of basic functionality
2. **tests/test_local.py**: Comprehensive test suite including:
   - Health check
   - Parse and score functionality
   - Explain terms endpoint
   - Deterministic output verification (same input = same hashes)

## Model Information

- **Default Model**: sentence-transformers/all-MiniLM-L6-v2
- **Embedding Dimension**: 384
- **Fallback**: TF-IDF vectorization (when ML_USE_FALLBACK=true)

## Architecture

```
ml_service/
├── app.py              # FastAPI application and endpoints
├── parser.py           # Resume anonymization and term extraction
├── vectorizer.py       # Similarity computation (transformer or TF-IDF)
├── hashing.py          # SHA-256 hash generation
├── job_desc.txt        # Sample job description
├── quick_test.py       # Quick test script
├── tests/
│   ├── test_local.py   # Comprehensive test suite
│   └── sample_resume.txt
└── requirements.txt    # Python dependencies
```

## Production Deployment

For production use with the full transformer model (default mode):

```bash
# The service will automatically download and cache the model on first startup
python app.py
```

Or explicitly set the environment variable:

```bash
# Explicitly use production mode
export ML_USE_FALLBACK=false
python app.py
```

The service will automatically download and cache the sentence-transformers model on first startup when internet access is available.
