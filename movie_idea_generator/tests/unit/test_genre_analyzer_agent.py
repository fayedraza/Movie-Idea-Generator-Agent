"""Tests for the GenreAnalyzerAgent."""

import pytest
from unittest.mock import patch, MagicMock

from src.agents.genre_analyzer_agent import GenreAnalyzerAgent


class TestGenreAnalyzerAgent:
    """Test the GenreAnalyzerAgent class."""
    
    def test_create(self):
        """Test creating a genre analyzer agent."""
        agent = GenreAnalyzerAgent.create()
        
        assert agent is not None
        assert agent.name == "Genre Analyzer Agent"
        assert "analyze" in agent.goal.lower()
        assert "genre" in agent.role.lower()
    
    def test_analyze_genres(self):
        """Test analyze_genres method returns expected genres."""
        agent = GenreAnalyzerAgent.create()
        
        # The mock will return ["Sci-Fi", "Drama", "Comedy"] - see conftest.py
        genres = agent.analyze_genres("A sci-fi movie about aliens")
        
        assert genres is not None
        assert isinstance(genres, list)
        assert len(genres) > 0
        assert all(isinstance(genre, str) for genre in genres)
    
    @patch('src.config.llm.get_openai_client')
    def test_analyze_genres_with_error(self, mock_get_client):
        """Test analyze_genres method when an error occurs."""
        # Make the mock client raise an exception
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("Test error")
        mock_get_client.return_value = mock_client
        
        agent = GenreAnalyzerAgent.create()
        genres = agent.analyze_genres("A sci-fi movie about aliens")
        
        # Should return default genres on error
        assert genres is not None
        assert isinstance(genres, list)
        assert len(genres) == 3  # Default is 3 genres
        assert "Drama" in genres
    
    def test_default_genres(self):
        """Test _default_genres method returns expected default genres."""
        agent = GenreAnalyzerAgent.create()
        
        genres = agent._default_genres()
        
        assert genres is not None
        assert isinstance(genres, list)
        assert len(genres) > 0
        assert "Drama" in genres 