from .base import RAGException


class ContentNotFoundException(RAGException):
    """Raised when requested content is not found in the knowledge base"""
    pass


class SessionExpiredException(RAGException):
    """Raised when a session has expired"""
    pass


class InvalidQueryException(RAGException):
    """Raised when a query is invalid or malformed"""
    pass


class RAGProcessingError(RAGException):
    """Raised when RAG processing fails"""
    pass