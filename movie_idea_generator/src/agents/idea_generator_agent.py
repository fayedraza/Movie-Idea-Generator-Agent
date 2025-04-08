"""Idea Generator Agent for generating movie ideas."""

import json
from typing import Dict, Optional

from src.config.llm import LLM, create_chat_completion


class IdeaGeneratorAgent:
    """Agent responsible for generating creative movie ideas."""

    @classmethod
    def create(cls):
        """
        Create a new idea generator agent.

        Returns:
            A new idea generator agent
        """
        agent = cls()
        agent.name = "Idea Generator Agent"
        agent.goal = "Generate creative movie ideas based on user prompts"
        agent.role = "Creative Content Strategist"
        agent.llm = LLM()
        return agent

    def generate_idea(self, prompt: str) -> Dict[str, str]:
        """
        Generate a movie idea based on the prompt.

        Args:
            prompt: The user's prompt for a movie idea

        Returns:
            Dictionary with the movie idea
        """
        try:
            # Create the messages list with the prompt
            messages = [
                {"role": "system", "content": "You are a creative movie idea generator."},
                {
                    "role": "user", 
                    "content": "Brainstorm creative movie concept ideas based on this prompt. "
                              "Focus on unique hooks, twists, or mashups that could make an interesting film: " + prompt
                }
            ]
            
            # Get completion using create_chat_completion
            response = create_chat_completion(
                messages=messages,
                model="gpt-3.5-turbo",
                temperature=0.8,
                max_tokens=500
            )
            
            # Extract and format the idea
            idea = response.choices[0].message.content
            
            return {"movie_idea": idea}
            
        except Exception as e:
            print(f"Error generating movie idea: {e}")
            # Return a default response if generation fails
            return self._create_default_idea()
            
    def _create_default_idea(self) -> Dict[str, str]:
        """
        Create a default movie idea when API calls fail.
        
        Returns:
            Dictionary containing a default movie idea
        """
        return {
            "movie_idea": "A person discovers they can communicate with objects, "
            "leading to unexpected adventures and insights into the human condition."
        } 