from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional, Dict, Any
from ..models import BookContent, SourceReference, Query as QueryModel
from ..utils import get_logger
from ..exceptions import RAGException, ContentNotFoundException, InvalidQueryException
from ..vector_db import get_qdrant_client
from qdrant_client.http import models
import openai
from ..config import settings


class RAGService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.logger = get_logger(__name__)
        self.qdrant_client = None  # Will be initialized when needed

    async def _get_qdrant_client(self):
        """Lazy initialization of Qdrant client."""
        if self.qdrant_client is None:
            self.qdrant_client = await get_qdrant_client()
        return self.qdrant_client

    async def process_query(
        self,
        query_text: str,
        session_id: Optional[UUID] = None,
        context_selection: Optional[str] = None,
        max_tokens: int = 500
    ):
        """Process a user query using RAG."""
        try:
            # Generate embedding for the query
            query_embedding = await self._generate_embedding(query_text)

            # Search for relevant content in Qdrant
            search_results = await self._search_similar_content(
                query_embedding,
                limit=5  # Top 5 most similar chunks
            )

            # Retrieve the actual content
            relevant_content = await self._get_content_by_ids(
                [result.payload["content_id"] for result in search_results]
            )

            # Generate response using OpenAI
            response_text = await self._generate_response(
                query_text,
                relevant_content,
                max_tokens
            )

            # Create source references
            sources = await self._create_source_references(search_results)

            # Save the query and response to database if session exists
            if session_id:
                await self._save_query_response(
                    session_id, query_text, response_text, sources
                )

            # Return the response
            from ..schemas.query import QueryResponse, SourceReference as SourceRefSchema
            return QueryResponse(
                response=response_text,
                sources=sources,
                session_id=session_id if session_id else UUID(int=0)  # Placeholder
            )
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            raise RAGException(f"Error processing query: {str(e)}")

    async def process_query_with_context(
        self,
        query_text: str,
        context_content_ids: List[UUID],
        session_id: Optional[UUID] = None
    ):
        """Process a query with specific context content."""
        try:
            # Retrieve specific content
            relevant_content = await self._get_content_by_ids(context_content_ids)

            # Generate response using OpenAI
            response_text = await self._generate_response(
                query_text,
                relevant_content,
                500  # Default max tokens
            )

            # Create source references
            sources = []  # Will be populated based on context_content_ids
            for content_id in context_content_ids:
                content = await self._get_content_by_id(content_id)
                if content:
                    sources.append({
                        "content_id": content_id,
                        "title": content.title,
                        "relevance_score": 1.0,  # All selected content is relevant
                        "text_preview": content.content[:200] + "..." if len(content.content) > 200 else content.content
                    })

            # Save the query and response to database if session exists
            if session_id:
                await self._save_query_response(
                    session_id, query_text, response_text, sources
                )

            # Return the response
            from ..schemas.query import QueryResponse, SourceReference as SourceRefSchema
            return QueryResponse(
                response=response_text,
                sources=sources,
                session_id=session_id if session_id else UUID(int=0)  # Placeholder
            )
        except Exception as e:
            self.logger.error(f"Error processing query with context: {str(e)}")
            raise RAGException(f"Error processing query with context: {str(e)}")

    async def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI."""
        try:
            openai.api_key = settings.openai_api_key
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response['data'][0]['embedding']
        except Exception as e:
            self.logger.error(f"Error generating embedding: {str(e)}")
            raise

    async def _search_similar_content(self, query_embedding: List[float], limit: int = 5):
        """Search for similar content in Qdrant."""
        try:
            qdrant = await self._get_qdrant_client()

            search_results = await qdrant.search(
                collection_name=settings.qdrant_collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True
            )

            return search_results
        except Exception as e:
            self.logger.error(f"Error searching similar content: {str(e)}")
            raise

    async def _get_content_by_ids(self, content_ids: List[UUID]) -> List[Dict[str, Any]]:
        """Get content by IDs from the database."""
        try:
            from sqlalchemy import select
            result = await self.db.execute(
                select(BookContent).where(BookContent.id.in_(content_ids))
            )
            contents = result.scalars().all()

            return [
                {
                    "id": content.id,
                    "title": content.title,
                    "content": content.content,
                    "module": content.module.title if content.module else "Unknown",
                    "chapter": content.chapter.title if content.chapter else "Unknown",
                    "section": content.section.title if content.section else "Unknown"
                }
                for content in contents
            ]
        except Exception as e:
            self.logger.error(f"Error getting content by IDs: {str(e)}")
            raise

    async def _get_content_by_id(self, content_id: UUID) -> Optional[BookContent]:
        """Get content by ID from the database."""
        try:
            from sqlalchemy import select
            result = await self.db.execute(
                select(BookContent).where(BookContent.id == content_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            self.logger.error(f"Error getting content by ID: {str(e)}")
            raise

    async def _generate_response(
        self,
        query: str,
        context: List[Dict[str, Any]],
        max_tokens: int
    ) -> str:
        """Generate response using OpenAI with context."""
        try:
            openai.api_key = settings.openai_api_key

            # Format context for the prompt
            context_text = "\n\n".join([
                f"Module: {item['module']}\nChapter: {item['chapter']}\nSection: {item['section']}\nContent: {item['content']}"
                for item in context
            ])

            prompt = f"""
            You are an AI assistant for an AI/Spec-Driven Book. Answer the user's question based only on the provided context.
            If the answer is not available in the context, clearly state that the information is not available in the book.

            Context:
            {context_text}

            Question: {query}

            Answer (with proper citations from the context):
            """

            response = openai.ChatCompletion.create(
                model=settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.3
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            raise

    async def _create_source_references(self, search_results) -> List[Dict[str, Any]]:
        """Create source references from search results."""
        sources = []
        for result in search_results:
            content_id = result.payload.get("content_id")
            if content_id:
                content = await self._get_content_by_id(UUID(content_id))
                if content:
                    sources.append({
                        "content_id": UUID(content_id),
                        "title": content.title,
                        "relevance_score": result.score,
                        "text_preview": result.payload.get("text", "")[:200] + "..."
                            if len(result.payload.get("text", "")) > 200
                            else result.payload.get("text", "")
                    })
        return sources

    async def _save_query_response(
        self,
        session_id: UUID,
        query_text: str,
        response_text: str,
        sources: List[Dict[str, Any]]
    ):
        """Save the query and response to the database."""
        try:
            from sqlalchemy import select
            # Verify session exists
            result = await self.db.execute(
                select(UserSession).where(UserSession.id == session_id)
            )
            session = result.scalar_one_or_none()
            if not session:
                raise ValueError(f"Session {session_id} not found")

            # Create query record
            query_record = QueryModel(
                session_id=session_id,
                query_text=query_text,
                response_text=response_text,
                sources=sources  # Store as JSON
            )

            self.db.add(query_record)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"Error saving query response: {str(e)}")
            raise