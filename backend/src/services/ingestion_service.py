from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Dict, Any
from ..models import BookContent, Module, Chapter, Section, Embedding
from ..utils import get_logger
from ..vector_db import get_qdrant_client
from ..services.chunking_service import ChunkingService
from ..services.embedding_service import EmbeddingService


class IngestionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.logger = get_logger(__name__)
        self.chunking_service = ChunkingService()
        self.embedding_service = EmbeddingService()

    async def ingest_content(
        self,
        content: str,
        module_id: UUID,
        chapter_id: UUID,
        section_id: UUID
    ) -> BookContent:
        """Ingest content and store it in the database."""
        try:
            # Verify that module, chapter, and section exist
            from sqlalchemy import select

            # Check module exists
            module_result = await self.db.execute(
                select(Module).where(Module.id == module_id)
            )
            module = module_result.scalar_one_or_none()
            if not module:
                raise ValueError(f"Module {module_id} not found")

            # Check chapter exists
            chapter_result = await self.db.execute(
                select(Chapter).where(Chapter.id == chapter_id)
            )
            chapter = chapter_result.scalar_one_or_none()
            if not chapter:
                raise ValueError(f"Chapter {chapter_id} not found")

            # Check section exists
            section_result = await self.db.execute(
                select(Section).where(Section.id == section_id)
            )
            section = section_result.scalar_one_or_none()
            if not section:
                raise ValueError(f"Section {section_id} not found")

            # Create book content record
            book_content = BookContent(
                module_id=module_id,
                chapter_id=chapter_id,
                section_id=section_id,
                title=f"Content for {section.title}",  # Generate title from section
                content=content,
                word_count=len(content.split())
            )

            self.db.add(book_content)
            await self.db.commit()
            await self.db.refresh(book_content)

            # Generate embeddings for the content
            await self._generate_embeddings(book_content)

            self.logger.info(f"Ingested content with ID: {book_content.id}")
            return book_content
        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"Error ingesting content: {str(e)}")
            raise

    async def ingest_content_with_chunking(
        self,
        content: str,
        module_id: UUID,
        chapter_id: UUID,
        section_id: UUID
    ):
        """Ingest content with section-aware chunking."""
        try:
            # Verify that module, chapter, and section exist
            from sqlalchemy import select

            # Check module exists
            module_result = await self.db.execute(
                select(Module).where(Module.id == module_id)
            )
            module = module_result.scalar_one_or_none()
            if not module:
                raise ValueError(f"Module {module_id} not found")

            # Check chapter exists
            chapter_result = await self.db.execute(
                select(Chapter).where(Chapter.id == chapter_id)
            )
            chapter = chapter_result.scalar_one_or_none()
            if not chapter:
                raise ValueError(f"Chapter {chapter_id} not found")

            # Check section exists
            section_result = await self.db.execute(
                select(Section).where(Section.id == section_id)
            )
            section = section_result.scalar_one_or_none()
            if not section:
                raise ValueError(f"Section {section_id} not found")

            # Chunk the content using section-aware strategy
            chunks = self.chunking_service.section_aware_chunk(content)

            # Process each chunk
            for i, chunk in enumerate(chunks):
                # Create book content record for each chunk
                book_content = BookContent(
                    module_id=module_id,
                    chapter_id=chapter_id,
                    section_id=section_id,
                    title=f"{section.title} - Chunk {i+1}",
                    content=chunk,
                    word_count=len(chunk.split())
                )

                self.db.add(book_content)
                await self.db.commit()
                await self.db.refresh(book_content)

                # Generate embeddings for this chunk
                await self._generate_embeddings(book_content)

            self.logger.info(f"Ingested content with chunking: {len(chunks)} chunks created")
            return {"status": "success", "chunks_created": len(chunks)}
        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"Error ingesting content with chunking: {str(e)}")
            raise

    async def _generate_embeddings(self, book_content: BookContent):
        """Generate embeddings for content and store in Qdrant."""
        try:
            # Generate embedding for the content
            embedding_vector = await self.embedding_service.generate_embedding(book_content.content)

            # Store in Qdrant
            qdrant = await get_qdrant_client()

            # Prepare point for Qdrant
            point = {
                "id": str(book_content.id),
                "vector": embedding_vector,
                "payload": {
                    "content_id": str(book_content.id),
                    "module_id": str(book_content.module_id),
                    "chapter_id": str(book_content.chapter_id),
                    "section_id": str(book_content.section_id),
                    "text": book_content.content,
                    "title": book_content.title
                }
            }

            # Upsert the point in Qdrant
            await qdrant.upsert(
                collection_name="book_content",
                points=[point]
            )

            # Also store in the embeddings table for reference
            embedding_record = Embedding(
                content_id=book_content.id,
                vector=embedding_vector,
                chunk_text=book_content.content,
                chunk_index=0  # For single content ingestion
            )
            self.db.add(embedding_record)
            await self.db.commit()

            self.logger.info(f"Generated embedding for content: {book_content.id}")
        except Exception as e:
            self.logger.error(f"Error generating embeddings: {str(e)}")
            raise