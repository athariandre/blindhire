"""
Shared configuration for ML service
"""
import os


# Whether to use TF-IDF fallback instead of sentence transformers
# Default is False for production use
USE_FALLBACK = os.environ.get('ML_USE_FALLBACK', 'false').lower() == 'true'


def get_model_name() -> str:
    """
    Get the model name based on current configuration
    """
    if USE_FALLBACK:
        return "tfidf-fallback"
    return "all-MiniLM-L6-v2"
