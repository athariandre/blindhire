import pytest
import os
from unittest.mock import patch, MagicMock

# Set environment variable to use fallback for testing
os.environ['ML_USE_FALLBACK'] = 'true'

from parser import anonymize_resume, extract_top_terms


class TestAnonymizeResume:
    """Test the anonymize_resume function"""
    
    def test_anonymize_basic_functionality(self):
        """Test basic anonymization functionality"""
        sample_text = """
        John Doe
        Email: john.doe@email.com
        Phone: (555) 123-4567
        MIT Computer Science Graduate
        """
        
        result = anonymize_resume(sample_text)
        
        # Should be a string
        assert isinstance(result, str)
        # Should contain redaction tokens
        assert "[REDACTED_EMAIL]" in result
        assert "[REDACTED_PHONE]" in result or "(555) 123-4567" not in result
        assert "[TARGET_SCHOOL]" in result
        # Should not contain the original email
        assert "john.doe@email.com" not in result
    
    def test_anonymize_with_gemini_success(self):
        """Test anonymization using Gemini API (mocked)"""
        sample_text = "John Doe, software engineer at TechCorp"
        expected_anonymized = "person, software engineer at company"
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            # Need to patch both gemini_model and the gemini configuration check
            with patch('parser.gemini_model') as mock_model, patch('parser.GEMINI_API_KEY', 'test_key'):
                mock_response = MagicMock()
                mock_response.text = expected_anonymized
                mock_model.generate_content.return_value = mock_response
                
                result = anonymize_resume(sample_text)
                
                assert result == expected_anonymized.lower()
                mock_model.generate_content.assert_called_once()
    
    def test_anonymize_with_gemini_fallback_on_error(self):
        """Test that anonymization falls back when Gemini fails"""
        sample_text = "John Doe john.doe@email.com"
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            with patch('parser.gemini_model') as mock_model, patch('parser.GEMINI_API_KEY', 'test_key'):
                mock_model.generate_content.side_effect = Exception("API Error")
                
                result = anonymize_resume(sample_text)
                
                # Should still process the text (fallback behavior)
                assert isinstance(result, str)
                assert "[REDACTED_EMAIL]" in result
    
    def test_anonymize_email_patterns(self):
        """Test that common email patterns are handled"""
        texts_with_emails = [
            "Contact me at john.doe@company.com for more info",
            "Email: JANE@COMPANY.COM",
            "Send to: user123@domain.org"
        ]
        
        for text in texts_with_emails:
            result = anonymize_resume(text)
            assert isinstance(result, str)
            assert "[REDACTED_EMAIL]" in result
    
    def test_anonymize_phone_patterns(self):
        """Test that phone number patterns are handled"""
        texts_with_phones = [
            "Call me at (555) 123-4567",
            "Phone: 555-123-4567",
            "Mobile: 555.123.4567"
        ]
        
        for text in texts_with_phones:
            result = anonymize_resume(text)
            assert isinstance(result, str)
            assert "[REDACTED_PHONE]" in result
    
    def test_anonymize_empty_and_whitespace(self):
        """Test anonymization with empty and whitespace-only text"""
        assert anonymize_resume("") == ""
        assert anonymize_resume("   ").strip() == ""
        assert anonymize_resume("\n\t\r").strip() == ""
    
    def test_anonymize_unicode_text(self):
        """Test anonymization with Unicode characters"""
        unicode_text = "José María González josé@company.com 中文 русский"
        result = anonymize_resume(unicode_text)
        
        assert isinstance(result, str)
        assert result.islower()
    
    def test_anonymize_preserves_technical_terms(self):
        """Test that technical terms are preserved"""
        technical_text = "Python programming React TensorFlow machine learning"
        result = anonymize_resume(technical_text)
        
        # Technical terms should be preserved (in lowercase)
        assert "python" in result
        assert "react" in result
        assert "tensorflow" in result
        assert "machine" in result
        assert "learning" in result


class TestExtractTopTerms:
    """Test the extract_top_terms function"""
    
    def test_extract_top_terms_basic(self):
        """Test basic top terms extraction"""
        text = "python programming software development machine learning python"
        result = extract_top_terms(text)
        
        assert isinstance(result, list)
        assert len(result) > 0
        # Should include frequent terms
        if len(result) > 0:
            # At least one term should be present
            assert any(term for term in result if len(term) > 0)
    
    def test_extract_top_terms_empty_text(self):
        """Test top terms extraction with empty text"""
        result = extract_top_terms("")
        
        assert isinstance(result, list)
        # Should handle empty text gracefully
    
    def test_extract_top_terms_single_word(self):
        """Test top terms extraction with single word"""
        result = extract_top_terms("python")
        
        assert isinstance(result, list)
    
    def test_extract_top_terms_with_count(self):
        """Test top terms extraction with custom count"""
        text = "python java javascript react node express flask django"
        
        # Test different numbers of terms
        result_3 = extract_top_terms(text, n=3)
        result_5 = extract_top_terms(text, n=5)
        
        assert isinstance(result_3, list)
        assert isinstance(result_5, list)
        assert len(result_3) <= 3
        assert len(result_5) <= 5
    
    def test_extract_top_terms_special_characters(self):
        """Test top terms extraction with special characters"""
        text = "C++ programming, Java/Python development, machine-learning"
        result = extract_top_terms(text)
        
        assert isinstance(result, list)
        # Should handle special characters gracefully


class TestAnonymizationEdgeCases:
    """Test edge cases for anonymization"""
    
    def test_very_long_text(self):
        """Test anonymization with very long text"""
        long_text = "This is a test sentence. " * 1000 + "john.doe@email.com"
        result = anonymize_resume(long_text)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_mixed_case_handling(self):
        """Test that mixed case is properly handled"""
        mixed_case_text = "JOHN DOE John.Doe@Company.COM Python PROGRAMMING"
        result = anonymize_resume(mixed_case_text)
        
        # Should contain redacted email token
        assert "[REDACTED_EMAIL]" in result
        # Technical terms should be preserved but normalized
        assert "python" in result
        assert "programming" in result
    
    def test_no_pii_text(self):
        """Test anonymization with text containing no PII"""
        clean_text = "Software engineer with experience in Python and machine learning"
        result = anonymize_resume(clean_text)
        
        # Should still normalize and lowercase
        assert result.islower()
        assert "software" in result
        assert "python" in result
        assert "machine" in result
        assert "learning" in result


class TestGeminiIntegration:
    """Test Gemini API integration (mocked)"""
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    def test_gemini_api_call_structure(self):
        """Test that Gemini is called with proper structure when available"""
        with patch('parser.gemini_model') as mock_model, patch('parser.GEMINI_API_KEY', 'test_key'):
            mock_response = MagicMock()
            mock_response.text = "anonymized text"
            mock_model.generate_content.return_value = mock_response
            
            test_text = "John Doe john@email.com"
            result = anonymize_resume(test_text)
            
            # Should have made a call to Gemini
            mock_model.generate_content.assert_called_once()
            
            # Result should be the mocked response
            assert result == "anonymized text"
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    def test_gemini_error_handling(self):
        """Test proper error handling when Gemini API fails"""
        with patch('parser.gemini_model') as mock_model:
            mock_model.generate_content.side_effect = Exception("Rate limit exceeded")
            
            test_text = "John Doe john@email.com"
            
            # Should not raise exception, should handle gracefully
            result = anonymize_resume(test_text)
            
            # Should return some processed text
            assert isinstance(result, str)
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': ''})
    def test_no_gemini_key_fallback(self):
        """Test that missing API key uses fallback processing"""
        test_text = "John Doe john@email.com"
        result = anonymize_resume(test_text)
        
        # Should still process the text
        assert isinstance(result, str)
        assert "[REDACTED_EMAIL]" in result or "john@email.com" not in result


if __name__ == "__main__":
    pytest.main([__file__])