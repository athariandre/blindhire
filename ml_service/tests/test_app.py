import pytest
import os
import tempfile
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json

# Set environment variable to use fallback for testing
os.environ['ML_USE_FALLBACK'] = 'true'

from app import app, load_job_description, determine_decision


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_resume():
    """Sample resume text for testing"""
    return """
    John Doe
    Email: john.doe@email.com
    Phone: (555) 123-4567
    
    EDUCATION
    MIT - Master of Science in Computer Science, 2023
    
    EXPERIENCE
    Software Engineer at TechCorp (2021-2023)
    - Developed machine learning models using Python and TensorFlow
    - Built scalable web applications with React and Node.js
    
    SKILLS
    Programming Languages: Python, JavaScript, Java
    Frameworks: React, TensorFlow, scikit-learn, FastAPI
    """


@pytest.fixture
def sample_job_description():
    """Sample job description for testing"""
    return """
    Senior Software Engineer Position
    
    Requirements:
    - 3+ years experience in Python development
    - Experience with machine learning frameworks
    - Knowledge of web application development
    - Familiarity with React and FastAPI
    """


@pytest.fixture
def mock_job_description_file(sample_job_description):
    """Mock job description file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(sample_job_description)
        temp_file = f.name
    
    # Patch the file path in the load_job_description function
    with patch('app.open', create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = sample_job_description
        yield temp_file
    
    # Clean up
    os.unlink(temp_file)


class TestHealthEndpoint:
    """Test the health check endpoint"""
    
    def test_health_endpoint_success(self, client):
        """Test health endpoint returns correct status and model info"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "model" in data
        assert "tfidf-fallback" in data["model"] or "all-MiniLM-L6-v2" in data["model"]
    
    def test_health_endpoint_content_type(self, client):
        """Test health endpoint returns JSON content type"""
        response = client.get("/health")
        
        assert response.headers["content-type"] == "application/json"


class TestParseAndScoreEndpoint:
    """Test the main parse_and_score endpoint"""
    
    def test_parse_and_score_success(self, client, sample_resume, mock_job_description_file):
        """Test successful parse and score request"""
        request_data = {
            "resume_text": sample_resume,
            "job_id": "test_job_123"
        }
        
        response = client.post("/parse_and_score", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields are present
        assert "similarity_score" in data
        assert "decision" in data
        assert "resume_hash" in data
        assert "model_hash" in data
        assert "score_hash" in data
        assert "explain" in data
        
        # Check data types and formats
        assert isinstance(data["similarity_score"], float)
        assert data["decision"] in ["auto_pass", "auto_fail", "review"]
        assert data["resume_hash"].startswith("0x")
        assert data["model_hash"].startswith("0x")
        assert data["score_hash"].startswith("0x")
        assert isinstance(data["explain"], dict)
        assert "top_terms" in data["explain"]
    
    def test_parse_and_score_custom_thresholds(self, client, sample_resume, mock_job_description_file):
        """Test parse and score with custom thresholds"""
        request_data = {
            "resume_text": sample_resume,
            "job_id": "test_job_123",
            "auto_pass_threshold": 0.8,
            "auto_fail_threshold": 0.2
        }
        
        response = client.post("/parse_and_score", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "similarity_score" in data
        assert "decision" in data
    
    def test_parse_and_score_missing_job_id(self, client, sample_resume):
        """Test parse and score with missing job_id"""
        request_data = {
            "resume_text": sample_resume
        }
        
        response = client.post("/parse_and_score", json=request_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_parse_and_score_missing_resume_text(self, client):
        """Test parse and score with missing resume_text"""
        request_data = {
            "job_id": "test_job_123"
        }
        
        response = client.post("/parse_and_score", json=request_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_parse_and_score_empty_resume(self, client, mock_job_description_file):
        """Test parse and score with empty resume text"""
        request_data = {
            "resume_text": "",
            "job_id": "test_job_123"
        }
        
        response = client.post("/parse_and_score", json=request_data)
        
        assert response.status_code == 200  # Should still process
        data = response.json()
        assert "similarity_score" in data
    
    @patch('app.load_job_description')
    def test_parse_and_score_job_not_found(self, mock_load_job, client, sample_resume):
        """Test parse and score with non-existent job"""
        from fastapi import HTTPException
        mock_load_job.side_effect = HTTPException(status_code=404, detail="Job not found")
        
        request_data = {
            "resume_text": sample_resume,
            "job_id": "nonexistent_job"
        }
        
        response = client.post("/parse_and_score", json=request_data)
        
        assert response.status_code == 404


class TestExplainTermsEndpoint:
    """Test the explain_terms endpoint"""
    
    def test_explain_terms_success(self, client, sample_resume):
        """Test successful explain terms request"""
        request_data = {
            "resume_text": sample_resume
        }
        
        response = client.post("/explain_terms", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "top_terms" in data
        assert isinstance(data["top_terms"], list)
    
    def test_explain_terms_empty_text(self, client):
        """Test explain terms with empty text"""
        request_data = {
            "resume_text": ""
        }
        
        response = client.post("/explain_terms", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "top_terms" in data
        assert isinstance(data["top_terms"], list)
    
    def test_explain_terms_missing_text(self, client):
        """Test explain terms with missing resume_text"""
        request_data = {}
        
        response = client.post("/explain_terms", json=request_data)
        
        assert response.status_code == 422  # Validation error


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_determine_decision_auto_pass(self):
        """Test decision determination for auto pass"""
        decision = determine_decision(0.8, auto_pass_threshold=0.75, auto_fail_threshold=0.3)
        assert decision == "auto_pass"
    
    def test_determine_decision_auto_fail(self):
        """Test decision determination for auto fail"""
        decision = determine_decision(0.2, auto_pass_threshold=0.75, auto_fail_threshold=0.3)
        assert decision == "auto_fail"
    
    def test_determine_decision_review(self):
        """Test decision determination for review"""
        decision = determine_decision(0.5, auto_pass_threshold=0.75, auto_fail_threshold=0.3)
        assert decision == "review"
    
    def test_determine_decision_edge_cases(self):
        """Test decision determination for edge cases"""
        # Exactly at threshold
        decision = determine_decision(0.75, auto_pass_threshold=0.75, auto_fail_threshold=0.3)
        assert decision == "auto_pass"
        
        decision = determine_decision(0.3, auto_pass_threshold=0.75, auto_fail_threshold=0.3)
        assert decision == "auto_fail"
    
    def test_load_job_description_success(self, sample_job_description):
        """Test successful job description loading"""
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = sample_job_description
            
            result = load_job_description("test_job")
            assert result == sample_job_description
    
    def test_load_job_description_file_not_found(self):
        """Test job description loading with missing file"""
        with patch('builtins.open', side_effect=FileNotFoundError()):
            with pytest.raises(Exception):  # Should raise HTTPException
                load_job_description("missing_job")


class TestIntegration:
    """Integration tests that test the full flow"""
    
    def test_full_workflow_integration(self, client, sample_resume, mock_job_description_file):
        """Test the complete workflow from request to response"""
        # First, check health
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # Then, explain terms
        explain_request = {"resume_text": sample_resume}
        explain_response = client.post("/explain_terms", json=explain_request)
        assert explain_response.status_code == 200
        
        # Finally, parse and score
        parse_request = {
            "resume_text": sample_resume,
            "job_id": "integration_test_job"
        }
        parse_response = client.post("/parse_and_score", json=parse_request)
        assert parse_response.status_code == 200
        
        # Verify the responses are consistent
        explain_data = explain_response.json()
        parse_data = parse_response.json()
        
        assert explain_data["top_terms"] == parse_data["explain"]["top_terms"]
    
    def test_multiple_requests_consistency(self, client, sample_resume, mock_job_description_file):
        """Test that multiple identical requests return consistent results"""
        request_data = {
            "resume_text": sample_resume,
            "job_id": "consistency_test_job"
        }
        
        # Make multiple requests
        response1 = client.post("/parse_and_score", json=request_data)
        response2 = client.post("/parse_and_score", json=request_data)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # These should be identical for the same input
        assert data1["similarity_score"] == data2["similarity_score"]
        assert data1["decision"] == data2["decision"]
        assert data1["resume_hash"] == data2["resume_hash"]
        assert data1["model_hash"] == data2["model_hash"]
        assert data1["score_hash"] == data2["score_hash"]


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_json_request(self, client):
        """Test handling of invalid JSON requests"""
        response = client.post("/parse_and_score", data="invalid json")
        assert response.status_code == 422
    
    def test_invalid_content_type(self, client):
        """Test handling of invalid content type"""
        response = client.post("/parse_and_score", data="some data", headers={"Content-Type": "text/plain"})
        assert response.status_code == 422
    
    def test_extremely_long_resume(self, client, mock_job_description_file):
        """Test handling of extremely long resume text"""
        long_resume = "word " * 10000  # Very long text
        request_data = {
            "resume_text": long_resume,
            "job_id": "test_job_long"
        }
        
        response = client.post("/parse_and_score", json=request_data)
        # Should still process but might be slow
        assert response.status_code in [200, 500]  # Might timeout or succeed
    
    def test_special_characters_resume(self, client, mock_job_description_file):
        """Test handling of resume with special characters"""
        special_resume = "José María González\n🚀 Software Engineer\n中文 русский العربية"
        request_data = {
            "resume_text": special_resume,
            "job_id": "test_job_special"
        }
        
        response = client.post("/parse_and_score", json=request_data)
        assert response.status_code == 200