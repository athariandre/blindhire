import requests
import json
import os


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
            print("✅ Explain terms working")
        else:
            print("Error:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to ML service")


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
    print("🧪 Testing ML Microservice")
    print("=" * 40)
    
    test_health()
    test_parse_and_score()
    test_explain_terms()
    test_deterministic_output()
    
    print("\n🎉 Tests completed!")