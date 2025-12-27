import asyncio
import argparse
import sys
import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Add the project root to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ..services.ingestion_service import IngestionService
from ..config import settings
from ..models import Module, Chapter, Section
import uuid


async def ingest_single_file(file_path: str, module_id: str, chapter_id: str, section_id: str):
    """Ingest a single file."""
    # Create database engine and session
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        # Create ingestion service
        ingestion_service = IngestionService(db)

        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"Ingesting {file_path}...")

        try:
            # Ingest the content
            result = await ingestion_service.ingest_content(
                content=content,
                module_id=uuid.UUID(module_id),
                chapter_id=uuid.UUID(chapter_id),
                section_id=uuid.UUID(section_id)
            )
            print(f"Successfully ingested {file_path} with ID: {result.id}")
        except Exception as e:
            print(f"Error ingesting {file_path}: {str(e)}")


async def ingest_directory(directory_path: str, module_id: str, chapter_id: str, section_id: str):
    """Ingest all markdown files in a directory."""
    directory = Path(directory_path)

    # Get all markdown files in the directory
    markdown_files = list(directory.glob("*.md"))

    print(f"Found {len(markdown_files)} markdown files to ingest")

    for file_path in markdown_files:
        await ingest_single_file(str(file_path), module_id, chapter_id, section_id)


def main():
    parser = argparse.ArgumentParser(description="CLI tool for bulk content ingestion")
    parser.add_argument("path", help="Path to file or directory to ingest")
    parser.add_argument("--module-id", required=True, help="Module ID for the content")
    parser.add_argument("--chapter-id", required=True, help="Chapter ID for the content")
    parser.add_argument("--section-id", required=True, help="Section ID for the content")
    parser.add_argument("--type", choices=["file", "directory"], default="file",
                        help="Type of path: file or directory (default: file)")

    args = parser.parse_args()

    # Validate UUIDs
    try:
        uuid.UUID(args.module_id)
        uuid.UUID(args.chapter_id)
        uuid.UUID(args.section_id)
    except ValueError:
        print("Error: Invalid UUID provided")
        sys.exit(1)

    # Check if path exists
    if not os.path.exists(args.path):
        print(f"Error: Path {args.path} does not exist")
        sys.exit(1)

    # Run the appropriate ingestion function
    if args.type == "file":
        asyncio.run(ingest_single_file(args.path, args.module_id, args.chapter_id, args.section_id))
    else:
        asyncio.run(ingest_directory(args.path, args.module_id, args.chapter_id, args.section_id))

    print("Ingestion completed!")


if __name__ == "__main__":
    main()