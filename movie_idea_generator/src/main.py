"""Main module for the movie idea generator."""

import json
import sys
from typing import Dict, List, Optional

from src.agents.genre_analyzer_agent import GenreAnalyzerAgent
from src.agents.idea_generator_agent import IdeaGeneratorAgent
from src.agents.recommendation_agent import RecommendationAgent
from src.config.env import check_api_keys


def generate_movie_idea(prompt: str) -> Dict:
    """
    Generate a movie idea based on the user prompt.

    Args:
        prompt: The user's prompt for a movie idea

    Returns:
        Dictionary with the movie idea generation results
    """
    # Create the agents
    genre_analyzer = GenreAnalyzerAgent.create()
    recommendation_agent = RecommendationAgent.create()
    idea_generator = IdeaGeneratorAgent.create()
    
    # Step 1: Analyze genres from the prompt
    genres = genre_analyzer.analyze_genres(prompt)
    print(f"Identified genres: {', '.join(genres)}")
    
    # Step 2: Get recommendations based on genres
    recommendations = recommendation_agent.get_recommendations(genres)
    print(f"Found recommendations: Movie '{recommendations['movie']['title']}' and Book '{recommendations['book']['title']}'")
    
    # Step 3: Generate movie idea based on prompt, genres, and recommendations
    movie_idea = idea_generator.generate_idea(prompt)
    
    # Return the complete result
    return {
        "user_prompt": prompt,
        "genres": genres,
        "recommendations": recommendations,
        "movie_idea": movie_idea["movie_idea"]
    }


def main():
    """Main entry point for the application."""
    # Check for required API keys
    if not check_api_keys():
        print("Missing required API keys. Please set them up before running the application.")
        sys.exit(1)
        # Return here to prevent execution of code below if we're testing
        # (sys.exit will stop execution in production but not in tests)
        return
    
    # Only get input from user if API keys are available
    prompt = input("Enter a movie idea prompt: ")
    
    # Generate movie idea
    result = generate_movie_idea(prompt)
    
    # Print the result
    print("\n==== MOVIE IDEA GENERATION RESULTS ====\n")
    print(f"Based on your prompt: '{result['user_prompt']}'")
    print(f"\nGenres: {', '.join(result['genres'])}")
    print("\nRecommendations:")
    print(f"  Movie: {result['recommendations']['movie']['title']} ({result['recommendations']['movie']['year']}) - {result['recommendations']['movie']['creator']}")
    print(f"  Book: {result['recommendations']['book']['title']} ({result['recommendations']['book']['year']}) - {result['recommendations']['book']['creator']}")
    print("\nYour Movie Idea:")
    print(f"{result['movie_idea']}")
    
    return result


if __name__ == "__main__":
    main() 