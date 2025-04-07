"""
Initialize the tests package.
"""

# Import stubs to help with import errors
try:
    import crewai
except ImportError:
    import sys
    from pathlib import Path
    current_dir = Path(__file__).parent
    if current_dir.joinpath('stubs.py').exists():
        from .stubs import Agent, Crew, Task, BaseTool, LLM
        sys.modules['crewai'] = type('crewai', (), {
            'Agent': Agent,
            'Crew': Crew,
            'Task': Task,
            'tools': type('tools', (), {'BaseTool': BaseTool}),
            'LLM': LLM
        })

# Import dotenv stub
try:
    from dotenv import load_dotenv
except ImportError:
    import sys
    from pathlib import Path
    current_dir = Path(__file__).parent
    if current_dir.joinpath('stubs.py').exists():
        from .stubs import load_dotenv
        sys.modules['dotenv'] = type('dotenv', (), {'load_dotenv': load_dotenv})

# Import requests stub
try:
    import requests
except ImportError:
    import sys
    from pathlib import Path
    current_dir = Path(__file__).parent
    if current_dir.joinpath('stubs.py').exists():
        from .stubs import post, Response
        sys.modules['requests'] = type('requests', (), {
            'post': post,
            'Response': Response
        })
