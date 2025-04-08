import json
from typing import Any, Dict, List, Optional

import requests
from crewai import LLM, Agent
from crewai.tools import BaseTool
from src.config.config import (
    OPENAI_MODELS,
    RECOMMENDATION_AGENT_CONFIG,
    RECOMMENDER_API_URL,
)
from src.config.llm import get_openai_client
from src.config.secrets import OPENAI_API_KEY


class RecommendationTool(BaseTool):
    name: str = "fetch_recommendations"
    description: str = (
        "Fetch movie and book recommendations from the API based on genres"
    )

    def _run(self, genres_str: str) -> Optional[Dict[str, Any]]:
        """Fetch recommendations from the API endpoint."""
        try:
            # Parse genres from the input string
            genres = [genre.strip() for genre in genres_str.split(",")]

            # Get movie recommendation
            movie_response = requests.post(
                f"{RECOMMENDER_API_URL}/recommend/",
                json={"type": "movies", "genres": genres},
            )
            movie_data = (
                movie_response.json() if movie_response.status_code == 200 else None
            )

            # Get book recommendation
            book_response = requests.post(
                f"{RECOMMENDER_API_URL}/recommend/",
                json={"type": "books", "genres": genres},
            )
            book_data = (
                book_response.json() if book_response.status_code == 200 else None
            )

            # If the API fails, generate fallback recommendations using OpenAI
            if movie_data is None or book_data is None:
                fallback = self.generate_fallback_recommendations(genres)

                if movie_data is None and "movie" in fallback:
                    movie_data = fallback["movie"]

                if book_data is None and "book" in fallback:
                    book_data = fallback["book"]

            return {"movie": movie_data, "book": book_data}
        except Exception:
            return None

    def generate_fallback_recommendations(self, genres: List[str]) -> Dict[str, Any]:
        """Generate fallback recommendations using OpenAI if the API fails."""
        try:
            # Get the OpenAI client
            client = get_openai_client()

            # Create a prompt for fallback recommendations
            genres_text = ", ".join(genres)

            # Use direct OpenAI client for generating fallback recommendations
            response = client.chat.completions.create(
                model=OPENAI_MODELS.get(
                    "gpt35_turbo",
                    "gpt-3.5-turbo",
                ),  # Use a faster model for recommendations
                messages=[
                    {
                        "role": "system",
                        "content": "You are a recommendation system for movies and books.",
                    },
                    {
                        "role": "user",
                        "content": f"Please recommend one movie and one book that match these genres: {genres_text}. Format the response as JSON with 'movie' and 'book' objects, each containing 'name', 'description', and 'genres' fields.",
                    },
                ],
                temperature=0.7,
                max_tokens=500,
                response_format={"type": "json_object"},
            )

            # Parse the JSON response
            content = response.choices[0].message.content
            return json.loads(content)

        except Exception:
            return {"movie": None, "book": None}


class RecommendationAgent:
    @staticmethod
    def create():
        # Create tool instance
        recommendation_tool = RecommendationTool()

        # Create an explicit LLM configuration object
        llm = LLM(
            model=OPENAI_MODELS.get("gpt35_turbo", "gpt-3.5-turbo"),
            temperature=RECOMMENDATION_AGENT_CONFIG.get("temperature", 0.5),
            api_key=OPENAI_API_KEY,
        )

        return Agent(
            role="Content Recommendation Specialist",
            goal="Find similar movies and books based on genre analysis",
            backstory="""You are a recommendation system expert who specializes in finding
            similar content based on genre analysis. You understand how to interpret genre
            profiles and use them to find the most relevant recommendations.""",
            tools=[recommendation_tool],
            verbose=True,
            llm=llm,  # Use explicit LLM object instead of llm_config
            **RECOMMENDATION_AGENT_CONFIG,
        )

    @staticmethod
    def get_recommendations(genres):
        """Get movie and book recommendations based on genres."""
