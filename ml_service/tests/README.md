# BlindHire ML Microservice Test Suite

This directory contains comprehensive tests for the BlindHire ML microservice, covering all components and functionality.

## Test Structure

### Test Files

- **`test_app.py`** - FastAPI application tests
  - Health endpoint testing
  - Parse and score endpoint testing
  - Explain terms endpoint testing
  - Request/response validation
  - Error handling
  - Integration tests

- **`test_parser.py`** - Resume parsing and anonymization tests
  - Regex-based anonymization
  - Gemini AI anonymization (mocked)
  - Top terms extraction
  - Edge cases and Unicode handling

- **`test_vectorizer.py`** - Text vectorization and similarity tests
  - TF-IDF fallback functionality
  - Sentence transformer integration (mocked)
  - Similarity computation
  - Model loading and caching

- **`test_hashing.py`** - Hash computation and integrity tests
  - SHA256 hash functions
  - Multi-component hash computation
  - Deterministic behavior
  - JSON payload structure

- **`test_config.py`** - Configuration management tests
  - Environment variable loading
  - Default value handling
  - Configuration validation

### Test Categories

#### Unit Tests
- Individual function testing
- Component isolation
- Input/output validation
- Edge case handling

#### Integration Tests
- End-to-end API workflows
- Component interaction
- Real request/response cycles
- Cross-component consistency

#### Error Handling Tests
- Invalid inputs
- Missing dependencies
- API failures
- Graceful degradation

## Running Tests

### Quick Start
```bash
# Run all tests
./run_tests.sh

# Or manually with pytest
pytest tests/ -v
```

### Individual Test Categories
```bash
# API endpoint tests
pytest tests/test_app.py -v

# Parser functionality tests
pytest tests/test_parser.py -v

# Vectorization tests
pytest tests/test_vectorizer.py -v

# Hash computation tests
pytest tests/test_hashing.py -v

# Configuration tests
pytest tests/test_config.py -v
```

### Test Options
```bash
# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run only fast tests (exclude slow/integration)
pytest tests/ -m "not slow"

# Run with detailed output
pytest tests/ -v -s

# Run specific test class
pytest tests/test_app.py::TestHealthEndpoint -v

# Run specific test function
pytest tests/test_parser.py::TestAnonymizeResume::test_anonymize_with_regex_fallback -v
```

## Test Environment

### Environment Variables
The tests automatically set up the following environment:
- `ML_USE_FALLBACK=true` - Uses TF-IDF instead of downloading models
- `GEMINI_API_KEY=""` - Disables Gemini API for testing

### Dependencies
- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `httpx` - HTTP client for FastAPI testing
- `unittest.mock` - Mocking framework

### Sample Data
- `tests/sample_resume.txt` - Sample resume for testing
- Mock job descriptions generated in tests
- Predefined test cases for various scenarios

## Test Coverage

### API Endpoints
✅ **Health Check** (`/health`)
- Status response validation
- Model information verification
- Content type checking

✅ **Parse and Score** (`/parse_and_score`)
- Successful processing workflows
- Custom threshold handling
- Input validation
- Error scenarios
- Response structure validation

✅ **Explain Terms** (`/explain_terms`)
- Term extraction functionality
- Empty input handling
- Response format validation

### Core Components
✅ **Resume Anonymization**
- Email removal
- Phone number removal
- Name pattern handling
- Gemini AI integration (mocked)
- Fallback mechanisms
- Unicode support

✅ **Text Vectorization**
- TF-IDF implementation
- Sentence transformer integration (mocked)
- Similarity computation
- Model loading and caching
- Error handling

✅ **Hash Computation**
- SHA256 implementation
- Multi-component hashing
- JSON payload structure
- Deterministic behavior
- Input validation

✅ **Configuration Management**
- Environment variable loading
- Default value handling
- Type validation
- Dynamic configuration

### Error Scenarios
✅ **Input Validation**
- Missing required fields
- Invalid data types
- Empty inputs
- Malformed requests

✅ **External Dependencies**
- Missing job descriptions
- API failures
- Model loading errors
- Network issues

✅ **Edge Cases**
- Very long texts
- Unicode characters
- Special characters
- Boundary conditions

## Mocking Strategy

### External APIs
- **Gemini AI**: Mocked to avoid API calls and costs
- **Sentence Transformers**: Mocked to avoid model downloads
- **File System**: Mocked for job description loading

### Benefits
- Fast test execution
- No external dependencies
- Consistent test results
- Offline capability

## Continuous Integration

The test suite is designed to run in CI/CD environments:
- No external API dependencies
- Deterministic results
- Fast execution (< 30 seconds)
- Clear pass/fail reporting

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx
```

**Model Download Errors**
```bash
# Ensure fallback mode is enabled
export ML_USE_FALLBACK=true
```

**Permission Errors**
```bash
# Make test script executable
chmod +x run_tests.sh
```

### Debug Mode
```bash
# Run with Python debugger
pytest tests/ --pdb

# Run with detailed logging
pytest tests/ -s --log-cli-level=DEBUG
```

## Contributing

When adding new functionality:
1. Add corresponding tests in appropriate test file
2. Follow existing test patterns and naming
3. Include both positive and negative test cases
4. Add edge case testing
5. Update this README if adding new test categories

### Test Naming Convention
- Test files: `test_<module>.py`
- Test classes: `Test<Functionality>`
- Test methods: `test_<specific_behavior>`

### Example Test Structure
```python
class TestNewFeature:
    def test_new_feature_success(self):
        """Test successful operation of new feature"""
        pass
    
    def test_new_feature_invalid_input(self):
        """Test new feature with invalid input"""
        pass
    
    def test_new_feature_edge_cases(self):
        """Test new feature edge cases"""
        pass
```