# Movie Idea Generator

A CrewAI-powered application that generates creative movie ideas based on user preferences.

## Overview

This application uses a team of AI agents to generate unique movie ideas:

1. **Genre Analyzer Agent**: Analyzes user preferences to identify relevant genres
2. **Recommendation Agent**: Finds movie and book recommendations based on the identified genres
3. **Idea Generator Agent**: Creates a unique movie concept by blending elements from the recommendations

## Flow

The application follows this flow:
1. User provides a prompt with movie preferences
2. Genre Analyzer identifies relevant genres from the prompt
3. Recommendation Agent suggests a movie and book that match these genres
4. Idea Generator creates a unique movie concept by combining elements from the recommendations

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application from the project root directory:

```
python -m movie_idea_generator.src.main
```

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

## Requirements

- Python 3.8+
- CrewAI
- Requests 