"""Recommendation Agent for suggesting movies and books."""

from typing import Dict, List, Optional

from src.config.llm import LLM, create_chat_completion


class RecommendationAgent:
    """Agent responsible for recommending movies and books based on genres."""

    @classmethod
    def create(cls):
        """
        Create a new recommendation agent.

        Returns:
            A new recommendation agent
        """
        agent = cls()
        agent.name = "Recommendation Agent"
        agent.goal = "Recommend relevant movies and books based on genre analysis"
        agent.role = "Content Recommendation Specialist"
        agent.llm = LLM()
        return agent

    def get_recommendations(self, genres: List[str]) -> Dict[str, Dict[str, str]]:
        """
        Get movie and book recommendations based on genres.

        Args:
            genres: List of genres to use for recommendations

        Returns:
            Dictionary with movie and book recommendations
        """
        try:
            # Create the messages list with the prompt
            genre_text = ", ".join(genres)
            messages = [
                {"role": "system", "content": "You are a content recommendation specialist."},
                {
                    "role": "user", 
                    "content": f"Recommend one movie and one book that match these genres: {genre_text}. "
                              f"Return a JSON object with 'movie' and 'book' objects, each containing 'title', "
                              f"'creator' (director/author), 'year', and 'description'."
                }
            ]
            
            # Get completion using create_chat_completion
            response = create_chat_completion(
                messages=messages,
                model="gpt-3.5-turbo",
                temperature=0.7,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            # Extract and format the recommendations
            content = response.choices[0].message.content
            
            # Try to parse the JSON response
            try:
                import json
                result = json.loads(content)
                
                # Validate and extract recommendations
                movie = result.get("movie", {})
                book = result.get("book", {})
                
                if not movie or not book:
                    return self._default_recommendations()
                
                return {
                    "movie": movie,
                    "book": book
                }
                
            except json.JSONDecodeError:
                # If JSON parsing fails, return default recommendations
                return self._default_recommendations()
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return self._default_recommendations()
            
    def _default_recommendations(self) -> Dict[str, Dict[str, str]]:
        """
        Provide default recommendations when API calls fail.
        
        Returns:
            Dictionary with default movie and book recommendations
        """
        return {
            "movie": {
                "title": "Inception",
                "creator": "Christopher Nolan",
                "year": "2010",
                "description": "A thief who steals corporate secrets through the use of dream-sharing technology."
            },
            "book": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "creator": "Douglas Adams",
                "year": "1979",
                "description": "A comedic science fiction series following the adventures of an unwitting human."
            }
        } 