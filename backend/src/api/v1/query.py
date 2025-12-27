from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from ...database import get_db
from ...schemas.query import QueryRequest, QueryResponse
from ...services.rag_service import RAGService


router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Query the RAG system with a user's question.
    """
    try:
        rag_service = RAGService(db)
        response = await rag_service.process_query(
            query_text=request.query,
            session_id=request.session_id,
            context_selection=request.context_selection,
            max_tokens=request.max_tokens
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/context", response_model=QueryResponse)
async def query_with_context(
    request: QueryRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Query the RAG system with specific context selection.
    """
    try:
        rag_service = RAGService(db)
        response = await rag_service.process_query_with_context(
            query_text=request.query,
            context_content_ids=request.context_content_ids or [],
            session_id=request.session_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))