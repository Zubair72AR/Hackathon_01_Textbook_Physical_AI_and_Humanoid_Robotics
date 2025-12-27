class RAGException(Exception):
    """Base exception for RAG-related errors"""
    pass


class ValidationError(RAGException):
    """Raised when input validation fails"""
    pass


class DatabaseError(RAGException):
    """Raised when database operations fail"""
    pass