#!/usr/bin/env python3
"""
Quick Gemini Integration Validator
Minimal test to verify Gemini anonymization is working
"""

import os
import sys

def validate_gemini_setup():
    """Quick validation of Gemini setup"""
    print("🔍 Validating Gemini Integration...")
    print("-" * 40)
    
    # Add parent directory to path
    sys.path.append('..')
    
    # Test 1: Configuration
    print("1. Testing Configuration...")
    try:
        from config import GEMINI_API_KEY, validate_config
        
        has_key = GEMINI_API_KEY is not None and len(GEMINI_API_KEY.strip()) > 0
        config_valid = validate_config()
        
        if has_key and config_valid:
            print("   ✅ Configuration OK")
        else:
            print("   ❌ Configuration Issue")
            if not has_key:
                print("      - Missing GEMINI_API_KEY in .env file")
            return False
            
    except Exception as e:
        print(f"   ❌ Config Error: {e}")
        return False
    
    # Test 2: Basic Anonymization
    print("\n2. Testing Basic Anonymization...")
    try:
        from parser import anonymize_resume
        
        test_input = "John Smith from MIT, email john@email.com, skilled in Python and React."
        result = anonymize_resume(test_input)
        
        # Quick checks
        pii_removed = "john" not in result.lower() and "smith" not in result.lower()
        skills_preserved = "python" in result.lower() and "react" in result.lower()
        
        if pii_removed and skills_preserved:
            print("   ✅ Anonymization Working")
            print(f"      Input:  {test_input}")
            print(f"      Output: {result[:60]}...")
        else:
            print("   ❌ Anonymization Issue")
            print(f"      PII Removed: {pii_removed}")
            print(f"      Skills Preserved: {skills_preserved}")
            print(f"      Result: {result}")
            return False
            
    except Exception as e:
        print(f"   ❌ Anonymization Error: {e}")
        return False
    
    # Test 3: Service Health (if running)
    print("\n3. Testing Service Integration...")
    try:
        import requests
        
        response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Service Running")
            
            # Quick service test
            payload = {
                "resume_text": "Jane Doe from Stanford, skilled in JavaScript",
                "job_id": "JOB-2025-001"
            }
            
            response = requests.post("http://127.0.0.1:8001/parse_and_score", 
                                   json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                required_fields = ["similarity_score", "decision", "resume_hash"]
                if all(field in result for field in required_fields):
                    print("   ✅ Service Integration OK")
                else:
                    print("   ❌ Service Response Missing Fields")
                    return False
            else:
                print(f"   ❌ Service Request Failed: {response.status_code}")
                return False
        else:
            print(f"   ⚠️  Service Not Running (Status: {response.status_code})")
            print("      This is OK if you haven't started the service yet")
            
    except requests.exceptions.ConnectionError:
        print("   ⚠️  Service Not Running")
        print("      This is OK if you haven't started the service yet")
    except Exception as e:
        print(f"   ❌ Service Test Error: {e}")
        return False
    
    print("\n🎉 Gemini Integration Validation Complete!")
    print("✅ All critical components are working correctly")
    return True

if __name__ == "__main__":
    print("🧪 Gemini Integration Quick Validator")
    print("=" * 50)
    
    if validate_gemini_setup():
        print("\n✅ SUCCESS: Gemini anonymization is ready to use!")
        print("\nNext steps:")
        print("- Start the ML service: uvicorn app:app --port 8001")
        print("- Run comprehensive tests: python test_gemini_anonymization.py")
        print("- Test with your own resume data")
    else:
        print("\n❌ ISSUES DETECTED: Please fix the problems above")
        print("\nTroubleshooting:")
        print("- Ensure GEMINI_API_KEY is set in .env file")
        print("- Check that python-dotenv is installed")
        print("- Verify your API key is valid and has quota")
        print("- Run: python -c 'from config import validate_config; validate_config()'")