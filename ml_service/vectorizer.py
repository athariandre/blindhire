from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# global model instance for efficiency
model = None


def load_model():
    """
    Load the sentence transformer model
    """
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model


def compute_similarity(resume_text: str, job_text: str) -> float:
    """
    Encode both strings using SentenceTransformer('all-MiniLM-L6-v2'),
    compute cosine similarity, return float rounded to 4 decimals.
    """
    # load model if not already loaded
    transformer = load_model()
    
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
    """
    return "all-MiniLM-L6-v2"
