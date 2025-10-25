#!/usr/bin/env python3
"""
ML Service Test Runner
Provides easy interface to run different categories of tests
"""

import sys
import os
import argparse

def run_basic_tests():
    """Run basic ML service tests"""
    print("🚀 Running Basic ML Service Tests...")
    
    # Add tests directory to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))
    from test_local import test_health, test_parse_and_score, test_explain_terms, test_deterministic_output
    
    results = []
    
    try:
        print("\n--- Health Check ---")
        test_health()
        results.append("Health: ✅")
    except Exception as e:
        print(f"❌ Health test failed: {e}")
        results.append("Health: ❌")
    
    try:
        print("\n--- Parse and Score ---")
        test_parse_and_score()
        results.append("Parse/Score: ✅")
    except Exception as e:
        print(f"❌ Parse/Score test failed: {e}")
        results.append("Parse/Score: ❌")
    
    try:
        print("\n--- Explain Terms ---")
        test_explain_terms()
        results.append("Explain: ✅")
    except Exception as e:
        print(f"❌ Explain test failed: {e}")
        results.append("Explain: ❌")
    
    try:
        print("\n--- Deterministic Output ---")
        test_deterministic_output()
        results.append("Deterministic: ✅")
    except Exception as e:
        print(f"❌ Deterministic test failed: {e}")
        results.append("Deterministic: ❌")
    
    print(f"\n📊 Basic Test Results: {', '.join(results)}")

def run_gemini_tests():
    """Run Gemini-specific tests"""
    print("🧠 Running Gemini Anonymization Tests...")
    
    # Add tests directory to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))
    from test_gemini_anonymization import run_gemini_tests as run_tests
    
    try:
        results = run_tests()
        return results['all_passed']
    except Exception as e:
        print(f"❌ Gemini tests failed: {e}")
        return False

def run_config_tests():
    """Run configuration tests"""
    print("🔧 Running Configuration Tests...")
    
    # Add tests directory to path  
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))
    from test_local import test_config_and_api_key
    
    try:
        return test_config_and_api_key()
    except Exception as e:
        print(f"❌ Config tests failed: {e}")
        return False

def run_anonymization_only():
    """Run only anonymization tests"""
    print("🕵️ Running Anonymization-Only Tests...")
    
    # Add tests directory to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))
    from test_local import test_gemini_anonymization
    
    try:
        return test_gemini_anonymization()
    except Exception as e:
        print(f"❌ Anonymization tests failed: {e}")
        return False

def check_service_status():
    """Check if ML service is running"""
    import requests
    try:
        response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        if response.status_code == 200:
            print("✅ ML Service is running on port 8001")
            return True
        else:
            print(f"❌ ML Service responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ ML Service is not running on port 8001")
        return False
    except Exception as e:
        print(f"❌ Error checking service: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="ML Service Test Runner")
    parser.add_argument("--test-type", choices=["basic", "gemini", "config", "anonymization", "all", "status"], 
                       default="all", help="Type of tests to run")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    print("🧪 ML Service Test Runner")
    print("=" * 40)
    
    if args.test_type == "status":
        check_service_status()
        return
    
    # Check service status first (except for config-only tests)
    if args.test_type != "config":
        service_running = check_service_status()
        if not service_running and args.test_type in ["basic", "all"]:
            print("⚠️  Warning: Some tests require the ML service to be running")
            print("   Start the service with: uvicorn app:app --port 8001")
            print()
    
    if args.test_type == "basic":
        run_basic_tests()
    elif args.test_type == "gemini":
        run_gemini_tests()
    elif args.test_type == "config":
        run_config_tests()
    elif args.test_type == "anonymization":
        run_anonymization_only()
    elif args.test_type == "all":
        print("Running comprehensive test suite...\n")
        
        config_ok = run_config_tests()
        print("\n" + "-" * 40)
        
        anonymization_ok = run_anonymization_only()
        print("\n" + "-" * 40)
        
        if check_service_status():
            run_basic_tests()
            print("\n" + "-" * 40)
        
        gemini_ok = run_gemini_tests()
        
        print("\n🎯 FINAL SUMMARY")
        print("=" * 40)
        print(f"Configuration: {'✅' if config_ok else '❌'}")
        print(f"Anonymization: {'✅' if anonymization_ok else '❌'}")
        print(f"Gemini Suite: {'✅' if gemini_ok else '❌'}")
        
        if config_ok and anonymization_ok and gemini_ok:
            print("\n🎉 All tests passed! Gemini integration is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()