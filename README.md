# Movie Ideas Recommender

This project consists of two components:

1. **Recommender API**: A FastAPI service for movie and book recommendations based on genres
2. **Movie Idea Generator**: A CrewAI application that generates creative movie concepts

## Quick Start Guide

### 1. Set Up and Run the Recommender API

```bash
# Navigate to the Recommender API directory
cd recommender_api

# Create and activate a virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Run the API server
cd app
uvicorn main:app --reload --port 8081
```

The API will be available at:
- http://localhost:8081/docs (Swagger UI)
- http://localhost:8081/redoc (ReDoc UI)

### 2. Set Up and Run the Movie Idea Generator

In a new terminal window:

```bash
# Navigate to the Movie Idea Generator directory
cd movie_idea_generator

# Using pip
pip install -e .

# Or using pipenv
# pipenv install
# pipenv shell

# Run the application
python run.py
```

When prompted, enter your movie preferences (e.g., "I want a sci-fi thriller with time travel").

### 3. Connect the Components (Optional)

By default, the Movie Idea Generator uses a placeholder API. To use your local Recommender API:

1. Edit `movie_idea_generator/src/config/config.py`:
   ```python
   RECOMMENDER_API_URL = "http://localhost:8081"
   ```

2. Ensure both services are running.

## Detailed Documentation

For more detailed instructions, see the README files in each component directory:

- [Recommender API Documentation](recommender_api/README.md)
- [Movie Idea Generator Documentation](movie_idea_generator/README.md) 