from crewai import LLM, Agent
from crewai.tools import BaseTool
from src.config.config import GENRE_ANALYZER_CONFIG, OPENAI_MODELS
from src.config.llm import get_openai_client
from src.config.secrets import OPENAI_API_KEY


class GenreAnalysisTool(BaseTool):
    name: str = "analyze_with_openai"
    description: str = (
        "Analyze text directly with OpenAI API to identify genres and themes"
    )

    def _run(self, text: str) -> str:
        """
        Analyze text directly with OpenAI API to identify genres and themes.
        This provides an additional tool for the agent to use.
        """
        try:
            # Get the OpenAI client
            client = get_openai_client()

            # Use direct OpenAI client for genre analysis
            response = client.chat.completions.create(
                model=OPENAI_MODELS.get("gpt4_turbo", "gpt-4-turbo"),
                messages=[
                    {
                        "role": "system",
                        "content": "You are a genre analysis expert who can identify the most relevant genres, themes, and narrative elements in text.",
                    },
                    {
                        "role": "user",
                        "content": f"Analyze the following content and identify the top 3-5 most relevant genres and key thematic elements:\n\n{text}",
                    },
                ],
                temperature=0.3,  # Low temperature for precise analysis
                max_tokens=1000,
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"Error analyzing with OpenAI: {str(e)}"


class GenreAnalyzerAgent:
    @staticmethod
    def create():
        # Create tool instance
        analysis_tool = GenreAnalysisTool()

        # Create an explicit LLM configuration object
        llm = LLM(
            model=OPENAI_MODELS.get("gpt4_turbo", "gpt-4-turbo"),
            temperature=GENRE_ANALYZER_CONFIG.get("temperature", 0.3),
            api_key=OPENAI_API_KEY,
        )

        return Agent(
            role="Genre Analysis Expert",
            goal="Analyze and determine the most relevant genres for given content",
            backstory="""You are an expert in content analysis and genre classification.
            Your specialty is identifying key themes, patterns, and genre elements in movies
            and books to determine their most accurate genre classifications.""",
            tools=[analysis_tool],
            verbose=True,
            llm=llm,  # Use explicit LLM object instead of llm_config
            **GENRE_ANALYZER_CONFIG,
        )

    @staticmethod
    def analyze_genres(user_prompt):
        """Analyze and determine genres for the user prompt."""
