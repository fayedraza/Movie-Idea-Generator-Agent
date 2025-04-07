import pytest
from unittest.mock import patch, MagicMock
import json
from src.agents.recommendation_agent import RecommendationAgent, RecommendationTool


class TestRecommendationTool:
    
    @patch('requests.post')
    def test_run_successful_api_call(self, mock_post):
        """Test _run method with successful API calls"""
        # Set up mock responses
        mock_movie_response = MagicMock()
        mock_movie_response.status_code = 200
        mock_movie_response.json.return_value = {
            "name": "Test Movie",
            "description": "Test movie description",
            "genres": ["Action", "Adventure"],
            "similarity_score": 0.8
        }
        
        mock_book_response = MagicMock()
        mock_book_response.status_code = 200
        mock_book_response.json.return_value = {
            "name": "Test Book",
            "description": "Test book description",
            "genres": ["Fantasy", "Adventure"],
            "similarity_score": 0.7
        }
        
        # Configure the mock to return different responses for different calls
        mock_post.side_effect = [mock_movie_response, mock_book_response]
        
        # Create the tool and call _run
        tool = RecommendationTool()
        result = tool._run("Action, Adventure")
        
        # Check the result
        assert result is not None
        assert "movie" in result
        assert "book" in result
        assert result["movie"]["name"] == "Test Movie"
        assert result["book"]["name"] == "Test Book"
        
        # Verify API calls
        assert mock_post.call_count == 2
    
    @patch('requests.post')
    @patch('src.agents.recommendation_agent.get_openai_client')
    def test_run_with_api_failure(self, mock_get_client, mock_post):
        """Test _run method with API failure, falling back to OpenAI"""
        # Set up API failure
        mock_post.return_value = MagicMock(status_code=500)
        
        # Set up OpenAI mock
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        
        # Set up the return structure for the fallback
        fallback_json = {
            "movie": {
                "name": "Fallback Movie",
                "description": "Fallback movie description",
                "genres": ["Action"]
            },
            "book": {
                "name": "Fallback Book",
                "description": "Fallback book description",
                "genres": ["Fantasy"]
            }
        }
        
        mock_message.content = json.dumps(fallback_json)
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_get_client.return_value = mock_client
        
        # Create the tool and call _run
        tool = RecommendationTool()
        result = tool._run("Action, Fantasy")
        
        # Check the result
        assert result is not None
        assert "movie" in result
        assert "book" in result
        assert result["movie"]["name"] == "Fallback Movie"
        assert result["book"]["name"] == "Fallback Book"
        
        # Verify that the client was called
        mock_client.chat.completions.create.assert_called_once()


class TestRecommendationAgent:
    
    def test_create(self):
        """Test the create method of RecommendationAgent"""
        with patch('src.agents.recommendation_agent.LLM') as mock_llm:
            # Mock the LLM class
            mock_llm_instance = MagicMock()
            mock_llm.return_value = mock_llm_instance
            
            # Call the create method
            agent = RecommendationAgent.create()
            
            # Verify that LLM was created correctly
            mock_llm.assert_called_once()
            
            # Verify the agent has the correct properties
            assert agent.role == 'Content Recommendation Specialist'
            assert 'recommendation' in agent.goal.lower()
            assert len(agent.tools) == 1
            assert isinstance(agent.tools[0], RecommendationTool)
    
    def test_get_recommendations(self):
        """Test the get_recommendations method"""
        # Call the method
        task_description = RecommendationAgent.get_recommendations("Action, Adventure")
        
        # Verify the result
        assert isinstance(task_description, str)
        assert "Action, Adventure" in task_description
        assert "fetch_recommendations" in task_description
        assert "MOVIE RECOMMENDATION" in task_description
        assert "BOOK RECOMMENDATION" in task_description 