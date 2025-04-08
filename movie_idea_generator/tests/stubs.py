"""
Stub implementations of external dependencies for testing.
This module provides simple mocks for external libraries that might not be installed.
"""


# Stub for crewai
class Agent:
    """Stub for crewai.Agent."""

    def __init__(self, **kwargs):
        self.role = kwargs.get("role", "")
        self.goal = kwargs.get("goal", "")
        self.backstory = kwargs.get("backstory", "")
        self.tools = kwargs.get("tools", [])
        self.verbose = kwargs.get("verbose", False)
        self.llm = kwargs.get("llm")


class Crew:
    """Stub for crewai.Crew."""

    def __init__(self, agents=None, tasks=None, verbose=False):
        self.agents = agents or []
        self.tasks = tasks or []
        self.verbose = verbose

    def kickoff(self):
        return "Test movie idea result"


class Task:
    """Stub for crewai.Task."""

    def __init__(self, description="", agent=None, expected_output=""):
        self.description = description
        self.agent = agent
        self.expected_output = expected_output


class BaseTool:
    """Stub for crewai.tools.BaseTool."""

    name = "stub_tool"
    description = "Stub tool for testing"

    def _run(self, *args, **kwargs):
        return None


class LLM:
    """Stub for crewai.LLM."""

    def __init__(self, model="", temperature=0.7, api_key=""):
        self.model = model
        self.temperature = temperature
        self.api_key = api_key


# Stubs for dotenv
def load_dotenv(*args, **kwargs):
    """Stub for dotenv.load_dotenv."""
    return True


# Stubs for requests
class Response:
    """Stub for requests.Response."""

    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}

    def json(self):
        return self._json_data


def post(url, json=None, **kwargs):
    """Stub for requests.post."""
    return Response(200, json)
