from unittest.mock import patch

from src.main import generate_movie_idea


class TestMovieIdeaWorkflow:
    @patch("src.agents.recommendation_agent.RecommendationTool._run")
    @patch("src.config.llm.create_chat_completion")
    def test_end_to_end_workflow(
        self,
        mock_chat_completion,
        mock_recommendation_tool_run,
    ):
        """Test the full workflow with mocked external dependencies."""
        # Set up OpenAI API mock responses
        mock_chat_completion.return_value = "Mocked OpenAI response for testing"

        # Set up the recommendation tool mock response
        mock_recommendation_tool_run.return_value = {
            "movie": {
                "name": "Test Movie",
                "description": "Test movie description",
                "genres": ["Action", "Adventure"],
            },
            "book": {
                "name": "Test Book",
                "description": "Test book description",
                "genres": ["Fantasy", "Adventure"],
            },
        }

        # Run the workflow with a test prompt
        result = generate_movie_idea("Test prompt with action and adventure elements")

        # Verify that the chat completion was called at least once
        assert mock_chat_completion.called

        # Verify that the recommendation tool was called
        mock_recommendation_tool_run.assert_called_once()

        # The result should be a string (the final movie idea)
        assert isinstance(result, str)
        assert len(result) > 0
