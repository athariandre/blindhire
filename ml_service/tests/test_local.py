import requests
import json
import os
import sys

# Import Gemini testing framework
from test_gemini_anonymization import GeminiAnonymizationTester


def test_parse_and_score():
    """
    Test the main parse_and_score endpoint
    """
    # read sample resume
    with open("tests/sample_resume.txt", "r") as f:
        resume_text = f.read()
    
    payload = {
        "resume_text": resume_text,
        "job_id": "JOB-2025-001"
    }
    
    try:
        response = requests.post("http://127.0.0.1:8001/parse_and_score", json=payload)
        print("Status Code:", response.status_code)
        
        if response.status_code == 200:
            result = response.json()
            print("Response:")
            print(json.dumps(result, indent=2))
            
            # validate response structure
            assert "similarity_score" in result
            assert "decision" in result
            assert "resume_hash" in result
            assert "model_hash" in result
            assert "score_hash" in result
            assert "explain" in result
            
            print("✅ All required fields present")
            
            # validate decision values
            assert result["decision"] in ["auto_pass", "auto_fail", "review"]
            print("✅ Valid decision category")
            
            # validate hash format
            assert result["resume_hash"].startswith("0x")
            assert result["model_hash"].startswith("0x")
            assert result["score_hash"].startswith("0x")
            print("✅ Hash format correct")
            
        else:
            print("Error:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to ML service. Make sure it's running on port 8001")


def test_health():
    """
    Test the health endpoint
    """
    try:
        response = requests.get("http://127.0.0.1:8001/health")
        print("\nHealth Check:")
        print("Status Code:", response.status_code)
        
        if response.status_code == 200:
            result = response.json()
            print("Response:", json.dumps(result, indent=2))
            assert result["status"] == "ok"
            print("✅ Health check passed")
        else:
            print("Error:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to ML service")


def test_explain_terms():
    """
    Test the explain_terms endpoint
    """
    with open("tests/sample_resume.txt", "r") as f:
        resume_text = f.read()
    
    payload = {"resume_text": resume_text}
    
    try:
        response = requests.post("http://127.0.0.1:8001/explain_terms", json=payload)
        print("\nExplain Terms:")
        print("Status Code:", response.status_code)
        
        if response.status_code == 200:
            result = response.json()
            print("Response:", json.dumps(result, indent=2))
            assert "top_terms" in result
            assert isinstance(result["top_terms"], list)
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to ML service")


def test_gemini_anonymization():
    """
    Test Gemini-powered anonymization functionality
    """
    print("\n🧠 Testing Gemini Anonymization...")
    
    # Quick anonymization test with known PII
    test_text = "John Smith from MIT, email john@email.com, skilled in Python and React."
    
    try:
        # Test direct anonymization
        sys.path.append('..')
        from parser import anonymize_resume
        
        anonymized = anonymize_resume(test_text)
        
        # Check that PII is removed but skills preserved
        pii_removed = "john" not in anonymized.lower() and "smith" not in anonymized.lower()
        skills_preserved = "python" in anonymized.lower() and "react" in anonymized.lower()
        school_anonymized = "[TARGET_SCHOOL]" in anonymized.lower()
        
        if pii_removed and skills_preserved and school_anonymized:
            print("✅ Gemini anonymization working correctly")
            print(f"  Original: {test_text[:50]}...")
            print(f"  Anonymized: {anonymized[:50]}...")
            return True
        else:
            print("❌ Gemini anonymization issues detected")
            print(f"  PII removed: {pii_removed}")
            print(f"  Skills preserved: {skills_preserved}")
            print(f"  School anonymized: {school_anonymized}")
            print(f"  Result: {anonymized}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing anonymization: {str(e)}")
        return False


def test_config_and_api_key():
    """
    Test that Gemini API key is properly configured
    """
    print("\n🔑 Testing Configuration...")
    
    try:
        sys.path.append('..')
        from config import validate_config, GEMINI_API_KEY
        
        # Test API key presence
        has_key = GEMINI_API_KEY is not None and len(GEMINI_API_KEY.strip()) > 0
        config_valid = validate_config()
        
        if has_key and config_valid:
            print("✅ Gemini API key configured correctly")
            return True
        else:
            print("❌ Configuration issues:")
            print(f"  Has API key: {has_key}")
            print(f"  Config valid: {config_valid}")
            return False
            
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False


def test_deterministic_output():
    """
    Test that the same input produces the same output (deterministic)
    """
    with open("tests/sample_resume.txt", "r") as f:
        resume_text = f.read()
    
    payload = {
        "resume_text": resume_text,
        "job_id": "JOB-2025-001"
    }
    
    try:
        # make two identical requests
        response1 = requests.post("http://127.0.0.1:8001/parse_and_score", json=payload)
        response2 = requests.post("http://127.0.0.1:8001/parse_and_score", json=payload)
        
        if response1.status_code == 200 and response2.status_code == 200:
            result1 = response1.json()
            result2 = response2.json()
            
            print("\nDeterministic Test:")
            print("First call hashes:")
            print(f"  Resume: {result1['resume_hash']}")
            print(f"  Model: {result1['model_hash']}")
            print(f"  Score: {result1['score_hash']}")
            
            print("Second call hashes:")
            print(f"  Resume: {result2['resume_hash']}")
            print(f"  Model: {result2['model_hash']}")
            print(f"  Score: {result2['score_hash']}")
            
            # check if all hashes are identical
            assert result1["resume_hash"] == result2["resume_hash"]
            assert result1["model_hash"] == result2["model_hash"]
            assert result1["score_hash"] == result2["score_hash"]
            assert result1["similarity_score"] == result2["similarity_score"]
            assert result1["decision"] == result2["decision"]
            
            print("✅ Deterministic output verified")
        else:
            print("❌ Failed to get successful responses for deterministic test")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to ML service")


if __name__ == "__main__":
    print("🧪 Testing ML Microservice with Gemini Integration")
    print("=" * 55)
    
    # Test configuration first
    config_ok = test_config_and_api_key()
    
    # Test basic service functionality
    test_health()
    test_parse_and_score()
    test_explain_terms()
    test_deterministic_output()
    
    # Test Gemini-specific functionality
    gemini_ok = test_gemini_anonymization()
    
    # Optionally run comprehensive Gemini tests
    print("\n" + "=" * 55)
    print("🔬 Running Comprehensive Gemini Test Suite...")
    
    try:
        gemini_tester = GeminiAnonymizationTester()
        gemini_results = gemini_tester.run_all_tests()
        
        print(f"\n📈 Overall Results:")
        print(f"  Configuration: {'✅' if config_ok else '❌'}")
        print(f"  Basic Anonymization: {'✅' if gemini_ok else '❌'}")
        print(f"  Comprehensive Tests: {'✅' if gemini_results['all_passed'] else '❌'}")
        print(f"  Success Rate: {gemini_results['success_rate']:.1f}%")
        
    except Exception as e:
        print(f"❌ Could not run comprehensive tests: {str(e)}")
    
    print("\n🎉 All tests completed!")