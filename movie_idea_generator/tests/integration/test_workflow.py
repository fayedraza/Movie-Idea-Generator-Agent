"""Integration tests for the movie idea workflow."""

import os
import pytest
from unittest.mock import patch, MagicMock

from src.main import generate_movie_idea


class TestMovieIdeaWorkflow:
    """Test the end-to-end movie idea generation workflow."""
    
    def test_end_to_end_workflow(self):
        """Test the entire workflow from prompt to final output."""
        # We don't need to mock create_chat_completion here since it's already mocked in conftest.py
        
        # Run the workflow
        result = generate_movie_idea("A sci-fi movie about communication between species")
        
        # Verify the result contains all expected sections
        assert result is not None
        assert "user_prompt" in result
        assert "genres" in result
        assert "recommendations" in result
        assert "movie_idea" in result
        
        # Check that genres list is populated
        assert isinstance(result["genres"], list)
        assert len(result["genres"]) > 0
        
        # Check recommendations
        assert "movie" in result["recommendations"]
        assert "book" in result["recommendations"]
        
        # Check movie idea is a string
        assert isinstance(result["movie_idea"], str)
        assert len(result["movie_idea"]) > 0 