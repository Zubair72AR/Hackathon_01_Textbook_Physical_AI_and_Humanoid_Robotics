from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from ...database import get_db
from ...services.ingestion_service import IngestionService


router = APIRouter()


@router.post("/")
async def ingest_content(
    content: str,
    module_id: UUID,
    chapter_id: UUID,
    section_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Ingest book content for RAG processing.
    """
    try:
        ingestion_service = IngestionService(db)
        result = await ingestion_service.ingest_content(
            content=content,
            module_id=module_id,
            chapter_id=chapter_id,
            section_id=section_id
        )
        return {"id": result.id, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chunk")
async def ingest_chunked_content(
    content: str,
    module_id: UUID,
    chapter_id: UUID,
    section_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Ingest content with custom chunking for RAG processing.
    """
    try:
        ingestion_service = IngestionService(db)
        result = await ingestion_service.ingest_content_with_chunking(
            content=content,
            module_id=module_id,
            chapter_id=chapter_id,
            section_id=section_id
        )
        return {"id": result.id, "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))