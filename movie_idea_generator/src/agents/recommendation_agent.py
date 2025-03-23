import requests
from crewai import Agent
from movie_idea_generator.src.config.config import RECOMMENDATION_AGENT_CONFIG, RECOMMENDER_API_URL

class RecommendationAgent:
    @staticmethod
    def create():
        return Agent(
            role='Content Recommendation Specialist',
            goal='Find similar movies and books based on genre analysis',
            backstory="""You are a recommendation system expert who specializes in finding 
            similar content based on genre analysis. You understand how to interpret genre 
            profiles and use them to find the most relevant recommendations.""",
            tools=[],
            verbose=True,
            **RECOMMENDATION_AGENT_CONFIG
        )

    @staticmethod
    def get_recommendations(genres):
        """Get movie and book recommendations based on genres"""
        task_description = f"""Using the following genres: {genres}
        
        Provide ONE movie and ONE book recommendation that best represent these genres.
        
        MOVIE RECOMMENDATION:
        1. Title: [Provide a well-known movie title]
        2. Director: [Director name]
        3. Year: [Release year]
        4. Synopsis: [Brief 2-3 sentence synopsis]
        5. Why it fits the genres: [Explain why this movie represents the genres well]
        6. Key elements: [List 3-5 key narrative elements, themes, or character dynamics]
        7. Unique aspects: [Identify 2-3 unique aspects that could inspire a new movie]
        
        BOOK RECOMMENDATION:
        1. Title: [Provide a well-known book title]
        2. Author: [Author name]
        3. Year: [Publication year]
        4. Synopsis: [Brief 2-3 sentence synopsis]
        5. Why it fits the genres: [Explain why this book represents the genres well]
        6. Key elements: [List 3-5 key narrative elements, themes, or character dynamics]
        7. Unique aspects: [Identify 2-3 unique aspects that could inspire a new movie]
        
        IMPORTANT: Choose recommendations that complement each other and could be combined to create an interesting new movie concept. The movie and book should be different enough to provide diverse inspiration but share thematic connections through the specified genres.
        """
        return task_description 