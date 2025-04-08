"""Tests for the main module."""

import pytest
import sys
from unittest.mock import patch, MagicMock

from src.main import generate_movie_idea, main


class TestMain:
    """Tests for the main module functions."""
    
    @patch('src.agents.genre_analyzer_agent.GenreAnalyzerAgent.analyze_genres')
    @patch('src.agents.recommendation_agent.RecommendationAgent.get_recommendations')
    @patch('src.agents.idea_generator_agent.IdeaGeneratorAgent.generate_idea')
    def test_generate_movie_idea(self, mock_generate_idea, mock_get_recommendations, mock_analyze_genres):
        """Test generate_movie_idea function."""
        # Setup mock returns
        mock_analyze_genres.return_value = ["Sci-Fi", "Drama"]
        mock_get_recommendations.return_value = {
            "movie": {
                "title": "Test Movie",
                "creator": "Test Director",
                "year": "2020",
                "description": "A test movie description"
            },
            "book": {
                "title": "Test Book",
                "creator": "Test Author",
                "year": "2010",
                "description": "A test book description"
            }
        }
        mock_generate_idea.return_value = {
            "movie_idea": "A test movie idea about a character who discovers a hidden world."
        }
        
        # Call the function
        result = generate_movie_idea("A sci-fi movie about aliens")
        
        # Check that mocks were called
        mock_analyze_genres.assert_called_once()
        mock_get_recommendations.assert_called_once()
        mock_generate_idea.assert_called_once()
        
        # Check result structure
        assert result is not None
        assert isinstance(result, dict)
        assert "user_prompt" in result
        assert "genres" in result
        assert "recommendations" in result
        assert "movie_idea" in result
        assert result["genres"] == ["Sci-Fi", "Drama"]
        assert result["recommendations"]["movie"]["title"] == "Test Movie"
        assert result["recommendations"]["book"]["title"] == "Test Book"
        assert "hidden world" in result["movie_idea"]
    
    @patch('src.main.generate_movie_idea')
    @patch('src.main.check_api_keys')
    @patch('builtins.input')
    def test_main(self, mock_input, mock_check_api_keys, mock_generate_movie_idea):
        """Test main function."""
        # Setup mocks
        mock_check_api_keys.return_value = True
        mock_input.return_value = "A sci-fi movie about aliens"
        mock_generate_movie_idea.return_value = {
            "user_prompt": "A sci-fi movie about aliens",
            "genres": ["Sci-Fi", "Drama"],
            "recommendations": {
                "movie": {
                    "title": "Test Movie",
                    "creator": "Test Director",
                    "year": "2020",
                    "description": "A test movie description"
                },
                "book": {
                    "title": "Test Book",
                    "creator": "Test Author",
                    "year": "2010",
                    "description": "A test book description"
                }
            },
            "movie_idea": "A test movie idea about a character who discovers a hidden world."
        }
        
        # Call the function
        result = main()
        
        # Check that mocks were called
        mock_check_api_keys.assert_called_once()
        mock_input.assert_called_once()
        mock_generate_movie_idea.assert_called_once_with("A sci-fi movie about aliens")
        
        # Check result
        assert result is not None
        assert isinstance(result, dict)
        assert "user_prompt" in result
        assert "genres" in result
        assert "recommendations" in result
        assert "movie_idea" in result
    
    def test_main_missing_api_keys(self):
        """Test main function when API keys are missing."""
        # Create patches but don't apply them yet
        check_api_keys_patcher = patch('src.main.check_api_keys', return_value=False)
        input_patcher = patch('builtins.input')
        exit_patcher = patch('sys.exit')
        
        # Start the patches
        mock_check_api_keys = check_api_keys_patcher.start()
        mock_input = input_patcher.start()
        mock_exit = exit_patcher.start()
        
        try:
            # Call the function
            main()
            
            # Check that sys.exit was called with the correct code
            mock_exit.assert_called_once_with(1)
            # Check that input was never called
            assert mock_input.call_count == 0, "Input should not be called when API keys are missing"
        finally:
            # Stop the patches
            check_api_keys_patcher.stop()
            input_patcher.stop()
            exit_patcher.stop() 