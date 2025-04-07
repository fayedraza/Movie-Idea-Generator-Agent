import pytest
from unittest.mock import patch, MagicMock
from src.main import generate_movie_idea, main


class TestMain:
    
    @patch('src.main.IdeaGeneratorAgent')
    @patch('src.main.GenreAnalyzerAgent')
    @patch('src.main.RecommendationAgent')
    @patch('src.main.Crew')
    def test_generate_movie_idea(self, mock_crew_class, mock_recommendation_agent,
                                mock_genre_analyzer, mock_idea_generator):
        """Test the generate_movie_idea function with mocked dependencies"""
        # Set up mocks
        mock_idea_generator_instance = MagicMock()
        mock_genre_analyzer_instance = MagicMock()
        mock_recommendation_agent_instance = MagicMock()
        
        mock_idea_generator.create.return_value = mock_idea_generator_instance
        mock_genre_analyzer.create.return_value = mock_genre_analyzer_instance
        mock_recommendation_agent.create.return_value = mock_recommendation_agent_instance
        
        mock_genre_analyzer.analyze_genres.return_value = "Mock genre analysis task"
        mock_recommendation_agent.get_recommendations.return_value = "Mock recommendation task"
        mock_idea_generator.generate_movie_idea.return_value = "Mock idea generation task"
        
        # Set up the mock crew
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "Generated movie idea result"
        mock_crew_class.return_value = mock_crew_instance
        
        # Call the function
        result = generate_movie_idea("Test prompt")
        
        # Verify that the agents were created
        mock_idea_generator.create.assert_called_once()
        mock_genre_analyzer.create.assert_called_once()
        mock_recommendation_agent.create.assert_called_once()
        
        # Verify that the crew was created and kickoff was called
        mock_crew_class.assert_called_once()
        mock_crew_instance.kickoff.assert_called_once()
        
        # Verify the result
        assert result == "Generated movie idea result"
    
    @patch('src.main.check_api_keys')
    @patch('src.main.generate_movie_idea')
    @patch('builtins.input')
    def test_main_successful(self, mock_input, mock_generate_movie_idea, mock_check_api_keys):
        """Test the main function with successful execution"""
        # Set up mocks
        mock_input.return_value = "Test prompt"
        mock_generate_movie_idea.return_value = "Generated movie idea"
        
        # Call the function
        with patch('builtins.print') as mock_print:
            main()
        
        # Verify that the API keys were checked
        mock_check_api_keys.assert_called_once()
        
        # Verify that input was called
        mock_input.assert_called_once()
        
        # Verify that generate_movie_idea was called with the correct argument
        mock_generate_movie_idea.assert_called_once_with("Test prompt")
        
        # Verify that print was called with the result
        mock_print.assert_any_call("\nGenerated Movie Idea:")
        mock_print.assert_any_call("Generated movie idea")
    
    @patch('src.main.check_api_keys')
    @patch('builtins.print')
    def test_main_exception(self, mock_print, mock_check_api_keys):
        """Test the main function with an exception"""
        # Set up mock to raise an exception
        mock_check_api_keys.side_effect = Exception("Test exception")
        
        # Call the function
        main()
        
        # Verify that print was called with the error message
        mock_print.assert_called_with("\nAn error occurred: Test exception") 