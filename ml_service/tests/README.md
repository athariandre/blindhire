# Gemini Anonymization Testing Guide

This directory contains a comprehensive testing framework for the Gemini-powered resume anonymization feature.

## Test Files

- `test_local.py` - Enhanced existing tests with Gemini integration
- `test_gemini_anonymization.py` - Comprehensive Gemini-specific test suite
- `test_runner.py` - Convenient test runner with different test categories

## Prerequisites

1. **Set up your Gemini API key** in `.env` file:
   ```bash
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

2. **Install dependencies** (if not already done):
   ```bash
   cd /Users/andre/Projects/competition/blindhire/ml_service
   source venv/bin/activate
   pip install python-dotenv
   ```

## Running Tests

### Quick Configuration Test
```bash
cd tests
python -c "
import sys
sys.path.append('..')
from config import validate_config
print('✅ Config OK' if validate_config() else '❌ Config Error')
"
```

### Basic Anonymization Test
```bash
cd tests
python -c "
import sys
sys.path.append('..')
from parser import anonymize_resume
test = 'John Smith from MIT skilled in Python'
result = anonymize_resume(test)
print(f'Input: {test}')
print(f'Output: {result}')
"
```

### Run Comprehensive Test Suite
```bash
cd tests
python test_gemini_anonymization.py
```

### Run Enhanced Local Tests
```bash
cd tests
python test_local.py
```

### Use Test Runner (various options)
```bash
# Check if service is running
python test_runner.py --test-type status

# Test only configuration
python test_runner.py --test-type config

# Test only anonymization
python test_runner.py --test-type anonymization

# Test everything
python test_runner.py --test-type all
```

## Test Categories

### 1. Configuration Tests
- Validates Gemini API key is loaded
- Checks environment variable configuration
- Verifies config validation functions

### 2. Anonymization Quality Tests
- Tests PII removal (names, emails, phones)
- Verifies technical skills preservation
- Validates school categorization (target vs non-target)
- Tests complex scenarios with mixed content

### 3. Service Integration Tests
- Tests full service endpoint with Gemini anonymization
- Validates response structure and deterministic behavior
- Checks hash consistency across calls

### 4. Fallback Behavior Tests
- Tests regex fallback when Gemini API is unavailable
- Validates graceful degradation

### 5. Performance Tests
- Benchmarks processing time for various resume lengths
- Validates performance within acceptable limits

## Expected Test Results

### Successful Gemini Integration
When Gemini is properly configured, you should see:
- ✅ Configuration tests pass
- ✅ PII removal with intelligent preservation of technical terms
- ✅ Service integration working correctly
- ✅ Deterministic hashing behavior
- ✅ Reasonable performance metrics

### Common Issues and Solutions

**❌ "GEMINI_API_KEY not set"**
- Solution: Add your API key to `.env` file in ml_service directory

**❌ "Could not connect to ML service"**
- Solution: Start the service with `uvicorn app:app --port 8001`

**❌ "Import errors"**
- Solution: Run tests from the `tests/` directory and ensure virtual environment is activated

**❌ Performance issues**
- Check internet connection (Gemini API requires network access)
- Verify API key has sufficient quota
- Consider using fallback mode for testing

## Example Test Output

```
🧪 GEMINI ANONYMIZATION TEST SUITE
==================================================
🔧 Testing Configuration...
✅ Environment Key Check: Gemini API key loaded
✅ Config Validation: Configuration valid

🧠 Testing Anonymization Quality...
✅ Anonymization - Personal Info Removal: PII removed: True, Skills preserved: True
✅ Anonymization - Technical Skills Preservation: PII removed: True, Skills preserved: True
✅ Anonymization - School Categorization: PII removed: True, Skills preserved: True

🌐 Testing Service Integration...
✅ Service Response Structure: All required fields present
✅ Deterministic Hashing: Hashes consistent across calls

📊 TEST SUMMARY
==============================
Total Tests: 12
Passed: 12
Failed: 0
Success Rate: 100.0%
```

## Integration with Existing Tests

The testing framework is designed to work alongside your existing test infrastructure:

- Extends `test_local.py` with new Gemini-specific tests
- Maintains all existing test functionality
- Provides both quick tests and comprehensive test suites
- Can be run independently or as part of broader testing

## Debugging Tips

1. **Enable verbose logging** in anonymization:
   ```python
   # In parser.py, add debug prints to see Gemini responses
   print(f"Gemini response: {response.text}")
   ```

2. **Test with different resume formats**:
   - Plain text resumes
   - Resumes with various PII patterns
   - Technical vs non-technical resumes

3. **Monitor API usage**:
   - Check Gemini API quotas and limits
   - Monitor response times
   - Track error rates

This testing framework ensures your Gemini integration is robust, performant, and ready for production use.