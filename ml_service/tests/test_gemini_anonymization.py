"""
Test framework for Gemini-powered resume anonymization
Builds on existing test infrastructure to validate AI anonymization
"""
import requests
import json
import os
import sys
import time
from typing import Dict, List, Tuple

# Add parent directory to path to import modules
sys.path.append('..')
from parser import anonymize_resume
from config import get_gemini_api_key, validate_config, GEMINI_API_KEY

class GeminiAnonymizationTester:
    """
    Comprehensive testing framework for Gemini-powered resume anonymization
    """
    
    def __init__(self):
        self.test_results = []
        self.service_url = "http://127.0.0.1:8001"
        
    def log_result(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "message": message
        })
        status = "✅" if passed else "❌"
        print(f"{status} {test_name}: {message}")

    def test_config_validation(self) -> bool:
        """Test that Gemini API key is properly configured"""
        print("\n🔧 Testing Configuration...")
        
        try:
            # Test environment variable loading
            has_key = GEMINI_API_KEY is not None and len(GEMINI_API_KEY.strip()) > 0
            self.log_result("Environment Key Check", has_key, 
                          "Gemini API key loaded" if has_key else "No API key found")
            
            # Test config validation function
            config_valid = validate_config()
            self.log_result("Config Validation", config_valid, 
                          "Configuration valid" if config_valid else "Configuration invalid")
            
            return has_key and config_valid
            
        except Exception as e:
            self.log_result("Config Validation", False, f"Error: {str(e)}")
            return False

    def test_anonymization_quality(self) -> bool:
        """Test the quality and effectiveness of Gemini anonymization"""
        print("\n🧠 Testing Anonymization Quality...")
        
        # Test cases with known PII that should be anonymized
        test_cases = [
            {
                "name": "Personal Info Removal",
                "input": "My name is John Smith, email john.smith@email.com, phone (555) 123-4567. I graduated from MIT with expertise in Python and React.",
                "should_not_contain": ["john", "smith", "john.smith@email.com", "(555) 123-4567", "mit"],
                "should_contain": ["python", "react", "[TARGET_SCHOOL]", "[REDACTED_EMAIL]", "[REDACTED_NAME]"]
            },
            {
                "name": "Technical Skills Preservation", 
                "input": "Andre Athari developed FastAPI applications using PostgreSQL, Docker, and deployed on AWS. Graduate of Stanford University.",
                "should_not_contain": ["andre", "athari", "stanford university"],
                "should_contain": ["fastapi", "postgresql", "docker", "aws", "[TARGET_SCHOOL]"]
            },
            {
                "name": "School Categorization",
                "input": "Sarah graduated from Harvard University with experience in machine learning. Also studied at Local Community College.",
                "should_not_contain": ["sarah", "harvard university", "local community college"],
                "should_contain": ["[TARGET_SCHOOL]", "[NON_TARGET_SCHOOL]", "machine learning"]
            },
            {
                "name": "Complex Contact Info",
                "input": "Contact Michael Johnson at m.johnson@company.com or 555.123.4567. MIT graduate skilled in TensorFlow and scikit-learn.",
                "should_not_contain": ["michael", "johnson", "m.johnson@company.com", "555.123.4567", "mit"],
                "should_contain": ["tensorflow", "scikit-learn", "[TARGET_SCHOOL]", "[REDACTED_EMAIL]", "[REDACTED_PHONE]"]
            }
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            try:
                # Test direct function call
                anonymized = anonymize_resume(test_case["input"])
                
                # Check that PII is removed
                pii_removed = True
                for should_not_have in test_case["should_not_contain"]:
                    if should_not_have.lower() in anonymized.lower():
                        pii_removed = False
                        break
                
                # Check that technical skills are preserved
                skills_preserved = True
                for should_have in test_case["should_contain"]:
                    if should_have.lower() not in anonymized.lower():
                        skills_preserved = False
                        break
                
                test_passed = pii_removed and skills_preserved
                all_passed = all_passed and test_passed
                
                result_msg = f"PII removed: {pii_removed}, Skills preserved: {skills_preserved}"
                if not test_passed:
                    result_msg += f"\nInput: {test_case['input'][:50]}...\nOutput: {anonymized[:50]}..."
                
                self.log_result(f"Anonymization - {test_case['name']}", test_passed, result_msg)
                
            except Exception as e:
                self.log_result(f"Anonymization - {test_case['name']}", False, f"Error: {str(e)}")
                all_passed = False
        
        return all_passed

    def test_service_integration(self) -> bool:
        """Test that the service correctly uses Gemini anonymization"""
        print("\n🌐 Testing Service Integration...")
        
        # Test data with clear PII
        test_resume = """
        John Doe
        Email: john.doe@email.com
        Phone: (555) 987-6543
        
        EDUCATION
        Harvard University - Computer Science, 2022
        Local State University - Mathematics, 2020
        
        SKILLS
        Python, JavaScript, React, TensorFlow, AWS, Docker
        
        EXPERIENCE
        Software Engineer at TechCorp
        - Developed machine learning models using Python and TensorFlow
        - Built web applications with React and FastAPI
        """
        
        try:
            # Test the main service endpoint
            payload = {
                "resume_text": test_resume,
                "job_id": "JOB-2025-001"
            }
            
            response = requests.post(f"{self.service_url}/parse_and_score", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # The service should have processed the resume through anonymization
                # We can't directly see the anonymized text, but we can verify the service responds correctly
                required_fields = ["similarity_score", "decision", "resume_hash", "model_hash", "score_hash"]
                has_all_fields = all(field in result for field in required_fields)
                
                self.log_result("Service Response Structure", has_all_fields, 
                              "All required fields present" if has_all_fields else "Missing fields")
                
                # Test that hashes are deterministic (same input should give same hash)
                response2 = requests.post(f"{self.service_url}/parse_and_score", json=payload, timeout=30)
                if response2.status_code == 200:
                    result2 = response2.json()
                    hashes_match = (result["resume_hash"] == result2["resume_hash"] and 
                                  result["score_hash"] == result2["score_hash"])
                    self.log_result("Deterministic Hashing", hashes_match, 
                                  "Hashes consistent across calls" if hashes_match else "Hash mismatch")
                    return has_all_fields and hashes_match
                else:
                    self.log_result("Service Integration", False, f"Second call failed: {response2.status_code}")
                    return False
            else:
                self.log_result("Service Integration", False, f"Service error: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.log_result("Service Integration", False, "Could not connect to ML service")
            return False
        except Exception as e:
            self.log_result("Service Integration", False, f"Unexpected error: {str(e)}")
            return False

    def test_fallback_behavior(self) -> bool:
        """Test behavior when Gemini API is not available"""
        print("\n🔄 Testing Fallback Behavior...")
        
        # Temporarily disable Gemini by modifying the module
        original_key = os.environ.get('GEMINI_API_KEY')
        
        try:
            # Test with no API key
            if 'GEMINI_API_KEY' in os.environ:
                del os.environ['GEMINI_API_KEY']
            
            # Import fresh parser module to test fallback
            import importlib
            sys.path.append('..')
            import parser
            importlib.reload(parser)
            
            test_text = "John Smith from MIT skilled in Python and React."
            anonymized = parser.anonymize_resume(test_text)
            
            # Should still work with regex fallback
            fallback_works = "[REDACTED_NAME]" in anonymized.lower()
            self.log_result("Fallback Anonymization", fallback_works, 
                          "Regex fallback working" if fallback_works else "Fallback failed")
            
            return fallback_works
            
        except Exception as e:
            self.log_result("Fallback Behavior", False, f"Error: {str(e)}")
            return False
        finally:
            # Restore original API key
            if original_key:
                os.environ['GEMINI_API_KEY'] = original_key

    def test_performance_benchmarks(self) -> bool:
        """Test performance of Gemini anonymization"""
        print("\n⚡ Testing Performance...")
        
        # Test with various resume sizes
        test_cases = [
            {"name": "Short Resume", "size": 200},
            {"name": "Medium Resume", "size": 1000}, 
            {"name": "Long Resume", "size": 2000}
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            try:
                # Generate test resume of specified size
                base_text = "John Doe from MIT skilled in Python. " * (test_case["size"] // 40)
                
                start_time = time.time()
                anonymized = anonymize_resume(base_text)
                end_time = time.time()
                
                processing_time = end_time - start_time
                
                # Performance thresholds (adjust as needed)
                time_limit = 10.0  # 10 seconds max
                performance_ok = processing_time < time_limit
                
                all_passed = all_passed and performance_ok
                
                self.log_result(f"Performance - {test_case['name']}", performance_ok,
                              f"Processed in {processing_time:.2f}s (limit: {time_limit}s)")
                
            except Exception as e:
                self.log_result(f"Performance - {test_case['name']}", False, f"Error: {str(e)}")
                all_passed = False
        
        return all_passed

    def run_all_tests(self) -> Dict:
        """Run complete test suite"""
        print("🧪 GEMINI ANONYMIZATION TEST SUITE")
        print("=" * 50)
        
        # Check if service is running
        try:
            health_response = requests.get(f"{self.service_url}/health", timeout=5)
            service_running = health_response.status_code == 200
        except:
            service_running = False
            
        if not service_running:
            print("⚠️  ML Service not running on port 8001. Some tests will be skipped.")
        
        # Run tests
        config_ok = self.test_config_validation()
        anonymization_ok = self.test_anonymization_quality()
        
        service_ok = True
        if service_running:
            service_ok = self.test_service_integration()
        
        fallback_ok = self.test_fallback_behavior()
        performance_ok = self.test_performance_benchmarks()
        
        # Summary
        print("\n📊 TEST SUMMARY")
        print("=" * 30)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["passed"])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if not result["passed"]]
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['message']}")
        
        return {
            "total": total_tests,
            "passed": passed_tests,
            "failed": total_tests - passed_tests,
            "success_rate": (passed_tests/total_tests)*100,
            "all_passed": passed_tests == total_tests,
            "results": self.test_results
        }


def run_gemini_tests():
    """Convenience function to run all Gemini tests"""
    tester = GeminiAnonymizationTester()
    return tester.run_all_tests()


if __name__ == "__main__":
    run_gemini_tests()