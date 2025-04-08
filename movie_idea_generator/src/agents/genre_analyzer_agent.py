"""Genre Analyzer Agent for analyzing and identifying movie genres."""

from typing import Dict, List, Optional

from src.config.llm import LLM, create_chat_completion


class GenreAnalyzerAgent:
    """Agent responsible for analyzing and identifying movie genres from user input."""

    @classmethod
    def create(cls):
        """
        Create a new genre analyzer agent.

        Returns:
            A new genre analyzer agent
        """
        agent = cls()
        agent.name = "Genre Analyzer Agent"
        agent.goal = "Analyze user input to identify potential movie genres"
        agent.role = "Genre Analysis Specialist"
        agent.llm = LLM()
        return agent

    def analyze_genres(self, prompt: str) -> List[str]:
        """
        Analyze the user prompt to identify relevant movie genres.

        Args:
            prompt: The user's prompt for a movie idea

        Returns:
            List of identified genres
        """
        try:
            # Create the messages list with the prompt
            messages = [
                {"role": "system", "content": "You are a genre analysis specialist for movies."},
                {
                    "role": "user", 
                    "content": f"Analyze this movie idea prompt and identify the most relevant genres. "
                              f"Return only a JSON array of genre names (2-4 genres): {prompt}"
                }
            ]
            
            # Get completion using create_chat_completion
            response = create_chat_completion(
                messages=messages,
                model="gpt-3.5-turbo",
                temperature=0.3,
                max_tokens=150,
                response_format={"type": "json_object"}
            )
            
            # Extract and format the genres
            content = response.choices[0].message.content
            
            # Try to parse the JSON response
            try:
                import json
                result = json.loads(content)
                genres = result.get("genres", [])
                if not genres:  # If "genres" key is not found, try to get the first array in the response
                    for key, value in result.items():
                        if isinstance(value, list):
                            genres = value
                            break
                
                return genres if genres else self._default_genres()
            except json.JSONDecodeError:
                # If JSON parsing fails, return default genres
                return self._default_genres()
            
        except Exception as e:
            print(f"Error analyzing genres: {e}")
            return self._default_genres()
            
    def _default_genres(self) -> List[str]:
        """
        Provide default genres when API calls fail.
        
        Returns:
            List of default genres
        """
        return ["Drama", "Adventure", "Comedy"] 