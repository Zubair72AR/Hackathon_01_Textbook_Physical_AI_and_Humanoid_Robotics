class RAGException(Exception):
    """Base exception for RAG-related errors"""
    pass


class ContentNotFoundException(RAGException):
    """Raised when requested content is not found in the knowledge base"""
    pass


class SessionExpiredException(RAGException):
    """Raised when a session has expired"""
    pass


class InvalidQueryException(RAGException):
    """Raised when a query is invalid or malformed"""
    pass