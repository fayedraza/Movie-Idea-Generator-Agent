"""
Initialize the tests package.
"""

# Import stubs to help with import errors
try:
    import fastapi
except ImportError:
    import sys
    from pathlib import Path
    current_dir = Path(__file__).parent
    if current_dir.joinpath('stubs.py').exists():
        from .stubs import FastAPI, HTTPException
        sys.modules['fastapi'] = type('fastapi', (), {
            'FastAPI': FastAPI,
            'HTTPException': HTTPException
        })

# Import pydantic stub
try:
    from pydantic import BaseModel, ValidationError
except ImportError:
    import sys
    from pathlib import Path
    current_dir = Path(__file__).parent
    if current_dir.joinpath('stubs.py').exists():
        from .stubs import BaseModel, ValidationError
        sys.modules['pydantic'] = type('pydantic', (), {
            'BaseModel': BaseModel,
            'ValidationError': ValidationError
        })

# Import numpy stub
try:
    import numpy
except ImportError:
    import sys
    from pathlib import Path
    current_dir = Path(__file__).parent
    if current_dir.joinpath('stubs.py').exists():
        from .stubs import NumpyStub
        sys.modules['numpy'] = NumpyStub()
        sys.modules['np'] = sys.modules['numpy']  # Common alias

# Import sklearn stubs
try:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    import sys
    from pathlib import Path
    current_dir = Path(__file__).parent
    if current_dir.joinpath('stubs.py').exists():
        from .stubs import CountVectorizer, cosine_similarity
        feature_extraction = type('text', (), {'CountVectorizer': CountVectorizer})
        metrics = type('pairwise', (), {'cosine_similarity': cosine_similarity})
        sys.modules['sklearn.feature_extraction.text'] = feature_extraction
        sys.modules['sklearn.metrics.pairwise'] = metrics
