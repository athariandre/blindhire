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

def test_parse_and_score():
    resume_text = """
    Andre Athari
    Email: andre.athari@email.com
    Phone: (555) 123-4567
    MIT graduate skilled in Python, machine learning, and SQL.
    Experience with React, cloud infrastructure on AWS.
    """
    
    payload = {
        "resume_text": resume_text,
        "job_id": "JOB-2025-001"
    }
    
    try:
        response = requests.post("http://127.0.0.1:8001/parse_and_score", json=payload, timeout=10)
        print(f"Parse and score endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("Response:")
            print(json.dumps(result, indent=2))
            return True
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Parse and score test failed: {e}")
    return False

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