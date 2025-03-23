from crewai import Agent
from movie_idea_generator.src.config.config import GENRE_ANALYZER_CONFIG

class GenreAnalyzerAgent:
    @staticmethod
    def create():
        return Agent(
            role='Genre Analysis Expert',
            goal='Analyze and determine the most relevant genres for given content',
            backstory="""You are an expert in content analysis and genre classification. 
            Your specialty is identifying key themes, patterns, and genre elements in movies 
            and books to determine their most accurate genre classifications.""",
            tools=[],
            verbose=True,
            **GENRE_ANALYZER_CONFIG
        )

    @staticmethod
    def analyze_genres(user_prompt):
        """Analyze and determine genres for the user prompt"""
        task_description = f"""Analyze the following user prompt and identify the most relevant genres for a movie idea:

        User Prompt: {user_prompt}
        
        Based on the user's preferences:
        
        1. PRIMARY GENRES (List 2-3 main genres):
           - [Genre 1]: [Brief explanation of why this is a primary genre]
           - [Genre 2]: [Brief explanation of why this is a primary genre]
           - [Genre 3]: [Brief explanation of why this is a primary genre]
        
        2. SECONDARY GENRES (List 1-2 supporting genres):
           - [Genre 4]: [Brief explanation of why this is a secondary genre]
           - [Genre 5]: [Brief explanation of why this is a secondary genre]
        
        3. KEY GENRE ELEMENTS TO INCLUDE:
           - [Element 1]: [Brief description]
           - [Element 2]: [Brief description]
           - [Element 3]: [Brief description]
        
        4. GENRE COMBINATIONS THAT WORK WELL:
           - [Combination 1]: [Why these genres work well together]
           - [Combination 2]: [Why these genres work well together]
        
        IMPORTANT: Focus on identifying genres that would help find relevant movie and book recommendations. Be specific and avoid overly broad genre classifications. Consider the emotional tone, themes, and narrative elements suggested by the user's prompt.
        """
        return task_description 