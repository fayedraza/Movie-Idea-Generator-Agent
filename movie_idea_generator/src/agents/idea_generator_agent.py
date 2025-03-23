from crewai import Agent
from movie_idea_generator.src.config.config import IDEA_GENERATOR_CONFIG

class IdeaGeneratorAgent:
    @staticmethod
    def create():
        return Agent(
            role='Creative Movie Idea Generator',
            goal='Generate creative movie ideas based on user preferences and recommendations',
            backstory="""You are a creative movie concept developer with extensive knowledge of 
            films and literature. Your job is to generate unique movie ideas by analyzing user 
            preferences and incorporating elements from similar content.""",
            tools=[],
            verbose=True,
            **IDEA_GENERATOR_CONFIG
        )

    @staticmethod
    def generate_movie_idea(user_prompt, genres, recommendations):
        """Generate a movie idea directly from user prompt, genres, and recommendations"""
        task_description = f"""Using the following inputs:
        1. User Prompt: {user_prompt}
        2. Analyzed Genres: {genres}
        3. Content Recommendations: {recommendations}
        
        The recommendations include both a movie and a book that match the genres.
        
        Create a unique movie concept that includes:
        1. Title
        2. Logline (one-sentence summary)
        3. Detailed synopsis (2-3 paragraphs)
        4. Target genres
        5. Key themes and elements
        6. Influences from the recommended movie and book (be specific about which elements you're drawing from each)
        
        The concept should blend elements from both the movie and book recommendations while 
        maintaining originality and addressing the user's prompt. Make sure to:
        
        - Draw narrative elements from the recommended movie
        - Draw thematic elements from the recommended book
        - Incorporate the genres identified by the genre analyzer
        - Stay true to the spirit of the user's original prompt
        
        Your final movie idea should be creative, marketable, and feel like a fresh concept rather than a derivative work.
        """
        return task_description 