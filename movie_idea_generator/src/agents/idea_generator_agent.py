import json
from typing import List

from crewai import LLM, Agent
from crewai.tools import BaseTool
from src.config.config import IDEA_GENERATOR_CONFIG, OPENAI_MODELS
from src.config.llm import create_chat_completion, get_openai_client
from src.config.secrets import OPENAI_API_KEY


class BrainstormTool(BaseTool):
    name: str = "brainstorm_with_openai"
    description: str = "Generate creative ideas directly with OpenAI API"

    def _run(self, prompt: str) -> str:
        """
        Generate creative ideas directly with OpenAI API.
        This provides an additional brainstorming tool for the agent.
        """
        try:
            # Use the create_chat_completion function from llm.py
            response = create_chat_completion(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a creative movie concept developer with expertise in storytelling, genre conventions, and cinematic techniques.",
                    },
                    {
                        "role": "user",
                        "content": f"Brainstorm creative movie concept ideas based on this prompt. Focus on unique hooks, twists, or mashups that could make an interesting film: {prompt}",
                    },
                ],
                model_key="gpt4_turbo",
                temperature=0.9,  # Higher temperature for more creativity
                max_tokens=1500,
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"Error brainstorming with OpenAI: {str(e)}"


class TitleGeneratorTool(BaseTool):
    name: str = "generate_title_options"
    description: str = "Generate multiple title options for a movie concept"

    def _run(self, concept: str, n: int = 5) -> List[str]:
        """Generate multiple title options for a movie concept using OpenAI."""
        try:
            # Get the OpenAI client
            client = get_openai_client()

            # Create completion for title generation
            response = client.chat.completions.create(
                model=OPENAI_MODELS.get(
                    "gpt35_turbo",
                    "gpt-3.5-turbo",
                ),  # Use a faster model for title generation
                messages=[
                    {
                        "role": "system",
                        "content": "You are a creative title generator for movies.",
                    },
                    {
                        "role": "user",
                        "content": f"Generate {n} potential titles for this movie concept. Return the result as a JSON array of strings: {concept}",
                    },
                ],
                temperature=0.8,
                max_tokens=300,
                response_format={"type": "json_object"},
            )

            # Parse the JSON response
            content = response.choices[0].message.content
            return json.loads(content).get("titles", [])
        except Exception as e:
            return [f"Error generating titles: {str(e)}"]


class IdeaGeneratorAgent:
    @staticmethod
    def create():
        # Create tool instances
        brainstorm_tool = BrainstormTool()
        title_generator_tool = TitleGeneratorTool()

        # Create an explicit LLM configuration object
        llm = LLM(
            model=OPENAI_MODELS.get("gpt4_turbo", "gpt-4-turbo"),
            temperature=IDEA_GENERATOR_CONFIG.get("temperature", 0.8),
            api_key=OPENAI_API_KEY,
        )

        return Agent(
            role="Creative Movie Idea Generator",
            goal="Generate creative movie ideas based on user preferences and recommendations",
            backstory="""You are a creative movie concept developer with extensive knowledge of
            films and literature. Your job is to generate unique movie ideas by analyzing user
            preferences and incorporating elements from similar content.""",
            tools=[brainstorm_tool, title_generator_tool],
            verbose=True,
            llm=llm,  # Use explicit LLM object instead of llm_config
            **IDEA_GENERATOR_CONFIG,
        )

    @staticmethod
    def generate_movie_idea(user_prompt, genres, recommendations):
        """Generate a movie idea directly from user prompt, genres, and recommendations."""
