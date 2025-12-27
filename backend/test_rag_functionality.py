"""
Test script for RAG functionality
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.services.rag_service import RAGService
from src.config import settings
import uuid


async def test_rag_functionality():
    """Test RAG functionality with sample queries."""

    # Create database engine and session
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        # Create RAG service
        rag_service = RAGService(db)

        # Test query
        test_query = "What are the fundamental communication patterns in ROS 2?"

        try:
            # This would normally require content to be ingested first
            # For now, we'll test the structure
            print("Testing RAG functionality...")
            print(f"Query: {test_query}")

            # In a real test, we would have ingested content first and then query it
            # This is a placeholder to show the intended functionality
            print("RAG service initialized successfully")
            print("Query processing would happen here with ingested content")

        except Exception as e:
            print(f"Error during RAG test: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_rag_functionality())