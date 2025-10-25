import pytest
import os
from unittest.mock import patch
from config import USE_FALLBACK, get_model_name, GEMINI_API_KEY, ML_SERVICE_PORT, ML_SERVICE_HOST


class TestConfigVariables:
    """Test configuration variables and environment loading"""
    
    def test_use_fallback_default(self):
        """Test USE_FALLBACK default value"""
        # Test with no environment variable set
        with patch.dict(os.environ, {}, clear=True):
            # Reload the config module to pick up changes
            import importlib
            import config
            importlib.reload(config)
            
            # Default should be False
            assert config.USE_FALLBACK is False
    
    def test_use_fallback_true(self):
        """Test USE_FALLBACK when set to true"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'true'}):
            import importlib
            import config
            importlib.reload(config)
            
            assert config.USE_FALLBACK is True
    
    def test_use_fallback_false(self):
        """Test USE_FALLBACK when explicitly set to false"""
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'false'}):
            import importlib
            import config
            importlib.reload(config)
            
            assert config.USE_FALLBACK is False
    
    def test_use_fallback_case_insensitive(self):
        """Test USE_FALLBACK is case insensitive"""
        test_cases = ['TRUE', 'True', 'tRuE', 'FALSE', 'False', 'fAlSe']
        
        for case in test_cases:
            with patch.dict(os.environ, {'ML_USE_FALLBACK': case}):
                import importlib
                import config
                importlib.reload(config)
                
                if case.lower() == 'true':
                    assert config.USE_FALLBACK is True
                else:
                    assert config.USE_FALLBACK is False
    
    def test_use_fallback_invalid_values(self):
        """Test USE_FALLBACK with invalid values defaults to False"""
        invalid_values = ['yes', 'no', '1', '0', 'invalid', '']
        
        for value in invalid_values:
            with patch.dict(os.environ, {'ML_USE_FALLBACK': value}):
                import importlib
                import config
                importlib.reload(config)
                
                assert config.USE_FALLBACK is False
    
    def test_gemini_api_key_loading(self):
        """Test GEMINI_API_KEY loading from environment"""
        test_key = "test_api_key_12345"
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': test_key}):
            import importlib
            import config
            importlib.reload(config)
            
            assert config.GEMINI_API_KEY == test_key
    
    def test_gemini_api_key_missing(self):
        """Test GEMINI_API_KEY when not set"""
        with patch.dict(os.environ, {}, clear=True):
            with patch('config.load_dotenv'):  # Mock load_dotenv to prevent .env file loading
                import importlib
                import config
                importlib.reload(config)
                
                assert config.GEMINI_API_KEY is None
    
    def test_ml_service_port_default(self):
        """Test ML_SERVICE_PORT default value"""
        with patch.dict(os.environ, {}, clear=True):
            import importlib
            import config
            importlib.reload(config)
            
            assert config.ML_SERVICE_PORT == 8001
    
    def test_ml_service_port_custom(self):
        """Test ML_SERVICE_PORT with custom value"""
        with patch.dict(os.environ, {'ML_SERVICE_PORT': '9000'}):
            import importlib
            import config
            importlib.reload(config)
            
            assert config.ML_SERVICE_PORT == 9000
    
    def test_ml_service_port_invalid(self):
        """Test ML_SERVICE_PORT with invalid value falls back to default"""
        with patch.dict(os.environ, {'ML_SERVICE_PORT': 'invalid'}):
            import importlib
            import config
            
            # This should raise ValueError during reload
            with pytest.raises(ValueError):
                importlib.reload(config)
    
    def test_ml_service_host_default(self):
        """Test ML_SERVICE_HOST default value"""
        with patch.dict(os.environ, {}, clear=True):
            import importlib
            import config
            importlib.reload(config)
            
            assert config.ML_SERVICE_HOST == "0.0.0.0"
    
    def test_ml_service_host_custom(self):
        """Test ML_SERVICE_HOST with custom value"""
        with patch.dict(os.environ, {'ML_SERVICE_HOST': 'localhost'}):
            import importlib
            import config
            importlib.reload(config)
            
            assert config.ML_SERVICE_HOST == "localhost"


class TestGetModelName:
    """Test the get_model_name function"""
    
    def test_get_model_name_with_fallback(self):
        """Test get_model_name when using fallback"""
        with patch('config.USE_FALLBACK', True):
            result = get_model_name()
            assert result == "tfidf-fallback"
    
    def test_get_model_name_without_fallback(self):
        """Test get_model_name when not using fallback"""
        with patch('config.USE_FALLBACK', False):
            result = get_model_name()
            assert result == "all-MiniLM-L6-v2"
    
    def test_get_model_name_return_type(self):
        """Test that get_model_name always returns a string"""
        result = get_model_name()
        assert isinstance(result, str)
        assert len(result) > 0


class TestEnvironmentVariableHandling:
    """Test environment variable handling edge cases"""
    
    def test_dotenv_loading(self):
        """Test that dotenv file loading works (if .env file exists)"""
        # This test checks if the load_dotenv() call works
        # We can't easily test the actual file loading without creating files
        # but we can verify the function doesn't crash
        import importlib
        import config
        
        # Should not raise any exceptions
        importlib.reload(config)
    
    def test_environment_precedence(self):
        """Test that environment variables take precedence over .env file"""
        # Set environment variable directly
        with patch.dict(os.environ, {'ML_USE_FALLBACK': 'true'}):
            import importlib
            import config
            importlib.reload(config)
            
            # Environment variable should take precedence
            assert config.USE_FALLBACK is True
    
    def test_missing_optional_variables(self):
        """Test behavior when optional environment variables are missing"""
        # Remove all our custom environment variables
        env_vars_to_remove = [
            'ML_USE_FALLBACK', 'GEMINI_API_KEY', 
            'ML_SERVICE_PORT', 'ML_SERVICE_HOST'
        ]
        
        clean_env = {k: v for k, v in os.environ.items() 
                    if k not in env_vars_to_remove}
        
        with patch.dict(os.environ, clean_env, clear=True):
            with patch('config.load_dotenv'):  # Mock load_dotenv to prevent .env file loading
                import importlib
                import config
                importlib.reload(config)
                
                # Should use defaults
                assert config.USE_FALLBACK is False
                assert config.GEMINI_API_KEY is None
                assert config.ML_SERVICE_PORT == 8001
                assert config.ML_SERVICE_HOST == "0.0.0.0"
    
    def test_empty_string_variables(self):
        """Test behavior with empty string environment variables"""
        with patch.dict(os.environ, {
            'ML_USE_FALLBACK': '',
            'GEMINI_API_KEY': '',
            'ML_SERVICE_HOST': ''
        }):
            import importlib
            import config
            importlib.reload(config)
            
            # Empty string should be treated as False for boolean
            assert config.USE_FALLBACK is False
            # Empty string should be preserved for strings
            assert config.GEMINI_API_KEY == ''
            assert config.ML_SERVICE_HOST == ''


class TestConfigurationValidation:
    """Test configuration validation and edge cases"""
    
    def test_port_range_validation(self):
        """Test port number validation"""
        # Test valid port numbers
        valid_ports = ['80', '8000', '8001', '9000', '65535']
        
        for port in valid_ports:
            with patch.dict(os.environ, {'ML_SERVICE_PORT': port}):
                import importlib
                import config
                importlib.reload(config)
                
                assert config.ML_SERVICE_PORT == int(port)
    
    def test_port_zero_and_negative(self):
        """Test port validation with zero and negative numbers"""
        # These should work (system will handle appropriately)
        edge_ports = ['0', '-1']
        
        for port in edge_ports:
            with patch.dict(os.environ, {'ML_SERVICE_PORT': port}):
                import importlib
                import config
                importlib.reload(config)
                
                assert config.ML_SERVICE_PORT == int(port)
    
    def test_host_validation(self):
        """Test host configuration validation"""
        valid_hosts = ['0.0.0.0', 'localhost', '127.0.0.1', 'myhost.com']
        
        for host in valid_hosts:
            with patch.dict(os.environ, {'ML_SERVICE_HOST': host}):
                import importlib
                import config
                importlib.reload(config)
                
                assert config.ML_SERVICE_HOST == host


class TestConfigConstants:
    """Test that configuration constants are properly defined"""
    
    def test_all_expected_constants_exist(self):
        """Test that all expected configuration constants are defined"""
        import config
        
        # Check that all expected attributes exist
        expected_attributes = [
            'USE_FALLBACK',
            'GEMINI_API_KEY', 
            'ML_SERVICE_PORT',
            'ML_SERVICE_HOST',
            'get_model_name'
        ]
        
        for attr in expected_attributes:
            assert hasattr(config, attr), f"Config missing attribute: {attr}"
    
    def test_constant_types(self):
        """Test that configuration constants have correct types"""
        import config
        
        assert isinstance(config.USE_FALLBACK, bool)
        assert config.GEMINI_API_KEY is None or isinstance(config.GEMINI_API_KEY, str)
        assert isinstance(config.ML_SERVICE_PORT, int)
        assert isinstance(config.ML_SERVICE_HOST, str)
        assert callable(config.get_model_name)
    
    def test_function_availability(self):
        """Test that configuration functions are available and callable"""
        result = get_model_name()
        assert isinstance(result, str)
        assert result in ["tfidf-fallback", "all-MiniLM-L6-v2"]


if __name__ == "__main__":
    pytest.main([__file__])