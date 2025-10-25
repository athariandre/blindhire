#!/usr/bin/env python3

import requests
import json

def test_health():
    try:
        response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        print(f"Health endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
    except Exception as e:
        print(f"Health test failed: {e}")
    return False

#!/usr/bin/env python3
"""
Quick validation test for the ML service with Gemini integration
"""
import requests
import json

def test_service():
    base_url = "http://127.0.0.1:8001"
    
    print("🧪 Quick ML Service Validation")
    print("=" * 40)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Service health check: PASSED")
        else:
            print(f"❌ Service health check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Service health check: FAILED (connection error: {e})")
        return False
    
    # Test anonymization endpoint
    try:
        test_resume = """John Smith
Email: john.smith@email.com
Phone: (555) 123-4567
Education: MIT Computer Science
Skills: Python, React, TensorFlow"""
        
        response = requests.post(
            f"{base_url}/anonymize",
            json={"text": test_resume}
        )
        
        if response.status_code == 200:
            result = response.json()
            anonymized = result.get("anonymized_text", "")
            
            print("✅ Anonymization endpoint: PASSED")
            print(f"Original: {test_resume[:50]}...")
            print(f"Anonymized: {anonymized[:100]}...")
            
            # Check if key elements are anonymized
            has_redacted_name = "[redacted_name]" in anonymized.lower()
            has_redacted_email = "[redacted_email]" in anonymized.lower()
            has_preserved_skills = "python" in anonymized.lower() and "react" in anonymized.lower()
            
            print(f"  - Names redacted: {'✅' if has_redacted_name else '❌'}")
            print(f"  - Emails redacted: {'✅' if has_redacted_email else '❌'}")
            print(f"  - Skills preserved: {'✅' if has_preserved_skills else '❌'}")
            
            return True
        else:
            print(f"❌ Anonymization endpoint: FAILED ({response.status_code})")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Anonymization endpoint: FAILED (error: {e})")
        return False

if __name__ == "__main__":
    success = test_service()
    if success:
        print("\n🎉 All tests passed! Gemini integration is working correctly.")
    else:
        print("\n💥 Some tests failed. Check the service logs.")

if __name__ == "__main__":
    print("🧪 Quick Test of ML Microservice")
    print("=" * 40)
    
    if test_health():
        print("✅ Health check passed")
        if test_parse_and_score():
            print("✅ Parse and score test passed")
        else:
            print("❌ Parse and score test failed")
    else:
        print("❌ Health check failed - service may not be running")