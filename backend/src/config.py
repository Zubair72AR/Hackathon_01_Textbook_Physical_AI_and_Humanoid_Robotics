from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql+asyncpg://user:password@localhost/book_db"
    neon_database_url: Optional[str] = None

    # Qdrant settings
    qdrant_url: Optional[str] = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "book_content"

    # OpenAI settings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"

    # Application settings
    app_name: str = "Unified AI Book RAG Chatbot"
    debug: bool = False
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS settings
    frontend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()