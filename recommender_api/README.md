# Genre-based Recommender API

This FastAPI application recommends movies or books based on genre similarity using semantic text similarity.

## Installation

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
   source venv/bin/activate
   ```

3. **Install the package in development mode**:
   ```bash
   # While in the recommender_api directory with activated environment
   pip install -e .
   ```

### Method 2: Using Hatch (Alternative)

```bash
# Install Hatch if you don't have it
brew install hatch

# Navigate to the project directory
cd recommender_api

# Install dependencies with Hatch
hatch env create
```

## Running the API

You can run the API in one of two ways:

### Option 1: From the app directory

```bash
# Navigate to the app directory
cd recommender_api/app

# Run the FastAPI application
uvicorn main:app --reload --port 8081
```

### Option 2: From the project root

```bash
# From the project root
cd recommender_api
python -m uvicorn app.main:app --reload --port 8081
```

To use a different port:

```bash
uvicorn app.main:app --reload --port <YOUR_PORT>
```

## API Documentation

After starting the server, access the documentation at:
- Interactive API docs: http://127.0.0.1:8081/docs
- ReDoc documentation: http://127.0.0.1:8081/redoc

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