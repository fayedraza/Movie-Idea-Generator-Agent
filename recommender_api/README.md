# Genre-based Recommender API

This FastAPI application recommends movies or books based on genre similarity using semantic text similarity.

## Setup and Installation

### Method 1: Using Python 3.12 with pip (Recommended)

1. **Install Python 3.12** (if not already installed):
   ```bash
   brew install python@3.12
   ```

2. **Set up a virtual environment**:
   ```bash
   # Navigate to the project directory
   cd recommender_api
   
   # Create a virtual environment
   python3.12 -m venv venv
   
   # Activate the virtual environment
   source venv/activate
   ```

3. **Install the package in development mode**:
   ```bash
   # While in the recommender_api directory with activated environment
   pip install -e .
   ```

### Method 2: Using Hatch (Alternative)

If you have Hatch installed:

```bash
# Install Hatch if you don't have it
brew install hatch

# Navigate to the project directory
cd recommender_api

# Install dependencies with Hatch
hatch env create
```

## Running the API

### With Python 3.12 (Recommended)

After setting up the environment as described above:

```bash
# Navigate to the app directory
cd app

# Run the FastAPI application
uvicorn main:app --reload --port 8081
```

Or from the project root:

```bash
python -m uvicorn app.main:app --reload --port 8081
```

### With Hatch (Alternative)

```bash
# From the recommender_api directory
hatch run run-api-alt
```

## Changing the Port

If you want to run the application on a different port:

```bash
uvicorn app.main:app --reload --port <YOUR_PORT>
```

## API Usage

### Endpoint: POST /recommend/

Request body:
```json
{
    "type": "movies",  // or "books"
    "genres": ["Action", "Adventure"]
}
```

Example response:
```json
{
    "name": "The Lord of the Rings",
    "description": "Epic fantasy adventure about a quest to destroy a powerful ring",
    "genres": ["Fantasy", "Adventure", "Action"],
    "similarity_score": 1.85
}
```

## Documentation

- API documentation is available at http://127.0.0.1:8081/docs
- ReDoc alternative documentation at http://127.0.0.1:8081/redoc 