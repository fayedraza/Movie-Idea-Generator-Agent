"""Tests for the RecommendationAgent."""

import pytest
from unittest.mock import patch, MagicMock

from src.agents.recommendation_agent import RecommendationAgent


class TestRecommendationAgent:
    """Tests for the RecommendationAgent class."""
    
    def test_create(self):
        """Test creating a recommendation agent."""
        agent = RecommendationAgent.create()
        
        assert agent is not None
        assert agent.name == "Recommendation Agent"
        assert "recommend" in agent.goal.lower()
        assert isinstance(agent.llm, object)
    
    def test_get_recommendations(self):
        """Test get_recommendations returns expected recommendations."""
        agent = RecommendationAgent.create()
        
        # Test with valid genres
        genres = ["Sci-Fi", "Drama", "Comedy"]
        result = agent.get_recommendations(genres)
        
        # Check for expected structure and data
        assert result is not None
        assert isinstance(result, dict)
        assert "movie" in result
        assert "book" in result
        assert "title" in result["movie"]
        assert "creator" in result["movie"]
        assert "year" in result["movie"]
        assert "description" in result["movie"]
        assert "title" in result["book"]
        assert "creator" in result["book"]
        assert "year" in result["book"]
        assert "description" in result["book"]
    
    @patch('src.config.llm.get_openai_client')
    def test_get_recommendations_with_api_failure(self, mock_get_client):
        """Test get_recommendations when API fails."""
        # Configure mock to raise exception
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API error")
        mock_get_client.return_value = mock_client
        
        agent = RecommendationAgent.create()
        genres = ["Sci-Fi", "Drama"]
        result = agent.get_recommendations(genres)
        
        # Should return fallback recommendations
        assert result is not None
        assert isinstance(result, dict)
        assert "movie" in result
        assert "book" in result
        assert result["movie"]["title"] == "Inception"
        assert result["book"]["title"] == "The Hitchhiker's Guide to the Galaxy"
    
    def test_default_recommendations(self):
        """Test _default_recommendations returns expected defaults."""
        agent = RecommendationAgent.create()
        
        defaults = agent._default_recommendations()
        
        # Check structure and content
        assert defaults is not None
        assert isinstance(defaults, dict)
        assert "movie" in defaults
        assert "book" in defaults
        assert defaults["movie"]["title"] == "Inception"
        assert defaults["book"]["title"] == "The Hitchhiker's Guide to the Galaxy" 