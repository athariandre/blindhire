import pytest
import numpy as np
from unittest.mock import patch, MagicMock
import os

# Set environment variable to use fallback for testing
os.environ['ML_USE_FALLBACK'] = 'true'

from vectorizer import (
    load_model, compute_similarity, get_model_identifier,
    model, tfidf_vectorizer
)


class TestLoadModel:
    """Test the model loading functionality"""
    
    def test_load_model_with_fallback(self):
        """Test loading model with TF-IDF fallback"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'true'}):
            # Reset global variables
            import vectorizer
            vectorizer.model = None
            vectorizer.tfidf_vectorizer = None
            
            result = load_model()
            
            # Should return TF-IDF vectorizer
            from sklearn.feature_extraction.text import TfidfVectorizer
            assert isinstance(result, TfidfVectorizer)
    
    def test_load_model_sentence_transformer(self):
        """Test loading sentence transformer model (mocked)"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'false'}):
            with patch('vectorizer.SentenceTransformer') as mock_st:
                mock_model = MagicMock()
                mock_st.return_value = mock_model
                
                # Reset global variables
                import vectorizer
                vectorizer.model = None
                vectorizer.tfidf_vectorizer = None
                
                result = load_model()
                
                assert result == mock_model
                mock_st.assert_called_once_with('all-MiniLM-L6-v2', local_files_only=False)
    
    def test_load_model_caching(self):
        """Test that model is cached after first load"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'true'}):
            # Reset and load first time
            import vectorizer
            vectorizer.model = None
            vectorizer.tfidf_vectorizer = None
            
            result1 = load_model()
            result2 = load_model()
            
            # Should return the same instance
            assert result1 is result2


class TestComputeSimilarity:
    """Test similarity computation"""
    
    def test_compute_similarity_with_fallback(self):
        """Test similarity computation using TF-IDF fallback"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'true'}):
            # Reset global variables
            import vectorizer
            vectorizer.model = None
            vectorizer.tfidf_vectorizer = None
            
            text1 = "software engineer python programming"
            text2 = "python developer programming software"
            
            similarity = compute_similarity(text1, text2)
            
            assert isinstance(similarity, float)
            assert 0.0 <= similarity <= 1.0
            # Similar texts should have higher similarity
            assert similarity > 0.5
    
    def test_compute_similarity_identical_texts(self):
        """Test similarity of identical texts"""
        text = "python programming software development"
        
        similarity = compute_similarity(text, text)
        
        assert isinstance(similarity, float)
        # Identical texts should have high similarity (close to 1.0)
        assert similarity > 0.9
    
    def test_compute_similarity_different_texts(self):
        """Test similarity of very different texts"""
        text1 = "python programming software development"
        text2 = "cooking recipes italian food"
        
        similarity = compute_similarity(text1, text2)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
        # Very different texts should have low similarity
        assert similarity < 0.5
    
    def test_compute_similarity_empty_texts(self):
        """Test similarity computation with empty texts"""
        # This should handle gracefully without crashing
        similarity = compute_similarity("", "some text")
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
        
        similarity = compute_similarity("some text", "")
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
        
        similarity = compute_similarity("", "")
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    def test_compute_similarity_sentence_transformer(self):
        """Test similarity computation with sentence transformer (mocked)"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'false'}):
            with patch('vectorizer.model') as mock_model:
                # Mock embeddings
                mock_model.encode.side_effect = [
                    np.array([[0.1, 0.2, 0.3]]),  # First text embedding
                    np.array([[0.2, 0.3, 0.4]])   # Second text embedding
                ]
                
                text1 = "python programming"
                text2 = "software development"
                
                with patch('vectorizer.cosine_similarity') as mock_cosine:
                    mock_cosine.return_value = np.array([[0.85]])
                    
                    similarity = compute_similarity(text1, text2)
                    
                    assert similarity == 0.85
                    assert mock_model.encode.call_count == 2
                    mock_cosine.assert_called_once()


class TestGetModelIdentifier:
    """Test model identifier function"""
    
    def test_get_model_identifier_fallback(self):
        """Test getting model identifier with fallback"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'true'}):
            identifier = get_model_identifier()
            
            assert isinstance(identifier, str)
            assert "tfidf" in identifier.lower()
    
    def test_get_model_identifier_sentence_transformer(self):
        """Test getting model identifier for sentence transformer"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'false'}):
            identifier = get_model_identifier()
            
            assert isinstance(identifier, str)
            assert "all-MiniLM-L6-v2" in identifier


class TestErrorHandling:
    """Test error handling in vectorizer"""
    
    def test_sentence_transformer_fallback_on_error(self):
        """Test fallback when sentence transformer fails to load"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'false'}):
            with patch('vectorizer.SentenceTransformer') as mock_st:
                mock_st.side_effect = Exception("Model not found")
                
                # Reset global variables
                import vectorizer
                vectorizer.model = None
                vectorizer.tfidf_vectorizer = None
                
                # Should fallback to TF-IDF
                result = load_model()
                
                from sklearn.feature_extraction.text import TfidfVectorizer
                assert isinstance(result, TfidfVectorizer)
    
    def test_compute_similarity_with_none_model(self):
        """Test similarity computation when model is None"""
        import vectorizer
        original_model = vectorizer.model
        original_tfidf = vectorizer.tfidf_vectorizer
        
        try:
            vectorizer.model = None
            vectorizer.tfidf_vectorizer = None
            
            # Should load model automatically
            similarity = compute_similarity("test text", "another test")
            assert isinstance(similarity, float)
            
        finally:
            # Restore original state
            vectorizer.model = original_model
            vectorizer.tfidf_vectorizer = original_tfidf


class TestTfidfFunctionality:
    """Test TF-IDF specific functionality"""
    
    def test_tfidf_vectorization(self):
        """Test TF-IDF vectorization process"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'true'}):
            # Reset global variables
            import vectorizer
            vectorizer.model = None
            vectorizer.tfidf_vectorizer = None
            
            texts = [
                "python programming software development",
                "machine learning artificial intelligence",
                "web development javascript react"
            ]
            
            # First call should fit the vectorizer
            similarity1 = compute_similarity(texts[0], texts[1])
            
            # Subsequent calls should use fitted vectorizer
            similarity2 = compute_similarity(texts[0], texts[2])
            
            assert isinstance(similarity1, float)
            assert isinstance(similarity2, float)
            assert 0.0 <= similarity1 <= 1.0
            assert 0.0 <= similarity2 <= 1.0
    
    def test_tfidf_max_features(self):
        """Test that TF-IDF respects max_features setting"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'true'}):
            # Reset global variables
            import vectorizer
            vectorizer.model = None
            vectorizer.tfidf_vectorizer = None
            
            vectorizer_instance = load_model()
            
            # Check max_features is set correctly
            assert vectorizer_instance.max_features == 384


class TestSentenceTransformerFunctionality:
    """Test Sentence Transformer specific functionality (mocked)"""
    
    def test_sentence_transformer_encoding(self):
        """Test sentence transformer encoding process"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'false'}):
            with patch('vectorizer.SentenceTransformer') as mock_st:
                mock_model = MagicMock()
                mock_st.return_value = mock_model
                
                # Mock encode method
                mock_model.encode.return_value = np.array([[0.1, 0.2, 0.3, 0.4]])
                
                # Reset global variables
                import vectorizer
                vectorizer.model = None
                vectorizer.tfidf_vectorizer = None
                
                # Load model
                load_model()
                
                # Test that encoding is called correctly
                text = "test text for encoding"
                
                with patch('vectorizer.cosine_similarity') as mock_cosine:
                    mock_cosine.return_value = np.array([[0.5]])
                    
                    similarity = compute_similarity(text, text)
                    
                    # Should call encode twice (for both texts)
                    assert mock_model.encode.call_count == 2


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_very_long_texts(self):
        """Test with very long input texts"""
        long_text = "word " * 1000
        
        similarity = compute_similarity(long_text, "short text")
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    def test_special_characters(self):
        """Test with texts containing special characters"""
        text1 = "C++ programming & software development!"
        text2 = "Python programming & web development?"
        
        similarity = compute_similarity(text1, text2)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    def test_unicode_texts(self):
        """Test with Unicode characters"""
        text1 = "Python programmation développement logiciel"
        text2 = "Desarrollo de software programación Python"
        
        similarity = compute_similarity(text1, text2)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    def test_single_word_texts(self):
        """Test with single word texts"""
        similarity = compute_similarity("python", "java")
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0


if __name__ == "__main__":
    pytest.main([__file__])