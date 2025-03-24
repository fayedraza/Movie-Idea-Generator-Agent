# Movie Idea Generator

A CrewAI-powered application that generates creative movie ideas based on user preferences.

## Overview

This application uses a team of AI agents to generate unique movie ideas:

1. **Genre Analyzer Agent**: Analyzes user preferences to identify relevant genres
2. **Recommendation Agent**: Finds movie and book recommendations based on the identified genres
3. **Idea Generator Agent**: Creates a unique movie concept by blending elements from the recommendations

## Installation

### Method 1: Using pip

1. **Navigate to the project directory**:
   ```bash
   cd movie_idea_generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

### Method 2: Using pipenv

1. **Navigate to the project directory**:
   ```bash
   cd movie_idea_generator
   ```

2. **Install dependencies**:
   ```bash
   pipenv install
   ```

3. **Activate the virtual environment**:
   ```bash
   pipenv shell
   ```

## Running the Application

There are two easy ways to run the application:

### Option 1: Using the run script

From the project root directory:

```bash
python movie_idea_generator/run.py
```

### Option 2: As a module

From the project root directory:

```bash
python -m movie_idea_generator.src.main
```

## Usage

When prompted, enter your movie idea preferences. For example:
- "I want a sci-fi thriller with time travel elements"
- "A romantic comedy set in a small town with supernatural elements"
- "An adventure story about a treasure hunt with philosophical themes"

The application will generate a detailed movie concept based on your preferences.

## Example Output

The generated movie idea will include:
- Title
- Logline (one-sentence summary)
- Detailed synopsis
- Target genres
- Key themes and elements
- Influences from the recommended movie and book

## API Integration

By default, the application uses a placeholder API. To connect it to the local Recommender API:

1. Update the `RECOMMENDER_API_URL` in `src/config/config.py`:
   ```python
   RECOMMENDER_API_URL = "http://localhost:8081"
   ```

2. Make sure the Recommender API is running (see the root README for instructions).

## Requirements

- Python 3.8+
- CrewAI
- Requests 