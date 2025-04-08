import pytest
from unittest.mock import patch, MagicMock
from src.config.env import check_api_keys


class TestEnv:
    
    @patch('src.config.secrets.OPENAI_API_KEY', 'valid-key')
    @patch('builtins.print')
    def test_check_api_keys_valid(self, mock_print):
        """Test check_api_keys with a valid API key"""
        # Call the function
        check_api_keys()
        
        # Verify that no warning was printed
        mock_print.assert_not_called()
    
    @patch('src.config.secrets.OPENAI_API_KEY', '')
    @patch('builtins.print')
    def test_check_api_keys_missing(self, mock_print):
        """Test check_api_keys with a missing API key"""
        # Call the function
        check_api_keys()
        
        # Verify that warnings were printed
        assert mock_print.call_count == 3
        mock_print.assert_any_call("\nWARNING: OPENAI_API_KEY is not set in the .env file.") 