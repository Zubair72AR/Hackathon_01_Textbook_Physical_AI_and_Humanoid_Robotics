"""
Test script for the ingestion pipeline
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models import BookContent, Module, Chapter, Section
from src.services.ingestion_service import IngestionService
from src.config import settings
import uuid


async def test_ingestion():
    """Test the ingestion pipeline with sample content."""

    # Create database engine and session
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        # Create a test module, chapter, and section
        test_module = Module(
            id=uuid.uuid4(),
            title="Test Module",
            description="A test module for ingestion",
            order=1
        )
        db.add(test_module)

        test_chapter = Chapter(
            id=uuid.uuid4(),
            module_id=test_module.id,
            title="Test Chapter",
            description="A test chapter for ingestion",
            order=1
        )
        db.add(test_chapter)

        test_section = Section(
            id=uuid.uuid4(),
            chapter_id=test_chapter.id,
            title="Test Section",
            description="A test section for ingestion",
            order=1
        )
        db.add(test_section)

        await db.commit()

        # Create ingestion service
        ingestion_service = IngestionService(db)

        # Sample content to ingest
        sample_content = """
# Introduction to Robotics

## What is a Robot?

A robot is a machine capable of carrying out complex actions automatically. Modern robots are typically programmable by a computer.

## Types of Robots

There are various types of robots:
- Industrial robots: Used in manufacturing
- Service robots: Assist humans in daily tasks
- Medical robots: Used in healthcare applications

## Humanoid Robots

Humanoid robots are robots with physical characteristics resembling humans. They often have:
- Two arms
- Two legs
- A head
- Sometimes facial features
        """

        try:
            # Test basic ingestion
            result = await ingestion_service.ingest_content(
                content=sample_content,
                module_id=test_module.id,
                chapter_id=test_chapter.id,
                section_id=test_section.id
            )
            print(f"Successfully ingested content with ID: {result.id}")

            # Test chunked ingestion
            result2 = await ingestion_service.ingest_content_with_chunking(
                content=sample_content,
                module_id=test_module.id,
                chapter_id=test_chapter.id,
                section_id=test_section.id
            )
            print(f"Successfully ingested content with chunking: {result2}")

        except Exception as e:
            print(f"Error during ingestion: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_ingestion())