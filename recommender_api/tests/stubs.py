"""
Stub implementations of external dependencies for testing.
This module provides simple mocks for external libraries that might not be installed.
"""

# Stubs for FastAPI
class FastAPI:
    """Stub for FastAPI class"""
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.version = kwargs.get('version', '0.1.0')
        self.routes = []
    
    def post(self, path, response_model=None, **kwargs):
        """Decorator for POST routes"""
        def decorator(func):
            self.routes.append((path, 'POST', func))
            return func
        return decorator

class HTTPException(Exception):
    """Stub for FastAPI HTTPException"""
    def __init__(self, status_code=400, detail="Error"):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"{status_code}: {detail}")

# Stubs for Pydantic
class BaseModel:
    """Stub for Pydantic BaseModel"""
    # Class attributes to define model fields
    __fields__ = {}
    __required_fields__ = []
    
    @classmethod
    def set_fields(cls, fields, required=None):
        """Set the fields for the model"""
        cls.__fields__ = fields
        cls.__required_fields__ = required or []
    
    def __init__(self, **data):
        # Check for required fields
        for field in self.__class__.__required_fields__:
            if field not in data:
                raise ValidationError(f"Field '{field}' is required")
        
        # Validate types if specified in fields
        for field, value in data.items():
            if field in self.__class__.__fields__:
                expected_type = self.__class__.__fields__[field]
                if expected_type and not isinstance(value, expected_type):
                    raise ValidationError(f"Field '{field}' should be of type {expected_type.__name__}")
        
        # Set attributes
        for key, value in data.items():
            setattr(self, key, value)
    
    def dict(self):
        """Convert model to dictionary"""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    @classmethod
    def validate(cls, data):
        """Validate the input data"""
        return cls(**data)

class ValidationError(Exception):
    """Stub for Pydantic ValidationError"""
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)

# Stub for numpy
class NumpyStub:
    """Stub for numpy module"""
    def __init__(self):
        self.array = lambda x: x
        self.ndarray = type('ndarray', (), {})
        self.float64 = float
        self.int64 = int

    def zeros(self, shape, dtype=None):
        """Create an array of zeros"""
        if isinstance(shape, int):
            return [0] * shape
        return [[0 for _ in range(shape[1])] for _ in range(shape[0])]

# Stubs for sklearn
class CountVectorizer:
    """Stub for sklearn.feature_extraction.text.CountVectorizer"""
    def fit_transform(self, raw_documents):
        """Return a simple identity matrix for testing"""
        return [[1 if i == j else 0 for j in range(len(raw_documents))] for i in range(len(raw_documents))]

def cosine_similarity(X, Y=None):
    """Stub for sklearn.metrics.pairwise.cosine_similarity"""
    # Return a simple similarity matrix for testing
    x_len = len(X)
    y_len = len(Y) if Y is not None else x_len
    return [[1.0 if i == j else 0.5 for j in range(y_len)] for i in range(x_len)] 