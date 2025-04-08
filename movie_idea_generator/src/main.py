from crewai import Crew, Task
# Import environment variables first to ensure API keys are loaded
from src.config.env import check_api_keys
from src.agents.idea_generator_agent import IdeaGeneratorAgent
from src.agents.genre_analyzer_agent import GenreAnalyzerAgent
from src.agents.recommendation_agent import RecommendationAgent

def generate_movie_idea(user_prompt):
    # Create agents
    idea_generator = IdeaGeneratorAgent.create()
    genre_analyzer = GenreAnalyzerAgent.create()
    recommendation_agent = RecommendationAgent.create()

    # Create tasks
    task1 = Task(
        description=GenreAnalyzerAgent.analyze_genres(user_prompt),
        agent=genre_analyzer,
        expected_output="List of relevant genres based on user prompt"
    )

    task2 = Task(
        description=RecommendationAgent.get_recommendations("{task1.output}"),
        agent=recommendation_agent,
        expected_output="Movie and book recommendations based on the identified genres"
    )

    task3 = Task(
        description=IdeaGeneratorAgent.generate_movie_idea(
            user_prompt,
            "{task1.output}",
            "{task2.output}"
        ),
        agent=idea_generator,
        expected_output="Final detailed movie concept"
    )

    # Create and run the crew
    crew = Crew(
        agents=[idea_generator, genre_analyzer, recommendation_agent],
        tasks=[task1, task2, task3],
        verbose=True
    )

    result = crew.kickoff()
    return result

def main():
    """Entry point for the movie idea generator."""
    try:
        # Check API keys before running
        check_api_keys()
        
        user_prompt = input("Please enter your movie idea preferences: ")
        result = generate_movie_idea(user_prompt)
        print("\nGenerated Movie Idea:")
        print(result)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main() 