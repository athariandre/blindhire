from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from config import USE_FALLBACK, get_model_name


# global model instance for efficiency
model = None
tfidf_vectorizer = None


def load_model():
    """
    Load the sentence transformer model or fallback to TF-IDF
    """
    global model, tfidf_vectorizer
    
    if USE_FALLBACK:
        # Use TF-IDF for testing when model unavailable
        if tfidf_vectorizer is None:
            tfidf_vectorizer = TfidfVectorizer(max_features=384)
        return tfidf_vectorizer
    
    if model is None:
        try:
            # Try to load from local cache or download
            model = SentenceTransformer('all-MiniLM-L6-v2', local_files_only=False)
        except Exception as e:
            print(f"Failed to load model: {e}")
            # Re-raise to let caller handle it
            raise RuntimeError(f"Model not available. Please ensure model is downloaded or internet is available: {e}")
    return model


def compute_similarity(resume_text: str, job_text: str) -> float:
    """
    Encode both strings using SentenceTransformer or TF-IDF fallback,
    compute cosine similarity, return float rounded to 4 decimals.
    """
    # load model if not already loaded
    transformer = load_model()
    
    if USE_FALLBACK:
        # Use TF-IDF approach
        try:
            tfidf_matrix = transformer.fit_transform([resume_text, job_text])
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            similarity_score = similarity_matrix[0][0]
        except Exception as e:
            print(f"Error in fallback similarity: {e}")
            return 0.5000
    else:
        # Use sentence transformers
        # encode both texts
        resume_embedding = transformer.encode([resume_text])
        job_embedding = transformer.encode([job_text])
        
        # compute cosine similarity
        similarity_matrix = cosine_similarity(resume_embedding, job_embedding)
        similarity_score = similarity_matrix[0][0]
    
    # round to 4 decimal places
    return round(float(similarity_score), 4)


def get_model_identifier() -> str:
    """
    Return the model identifier for consistent hashing
    Reflects the actual model being used (transformer or fallback)
    """
    return get_model_name()
