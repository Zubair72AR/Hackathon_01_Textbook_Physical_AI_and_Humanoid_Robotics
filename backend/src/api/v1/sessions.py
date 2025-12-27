from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from ...database import get_db
from ...schemas.session import SessionResponse, SessionHistoryResponse
from ...services.session_service import SessionService


router = APIRouter()


@router.post("/", response_model=SessionResponse)
async def create_session(
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user session for conversation history.
    """
    try:
        session_service = SessionService(db)
        session = await session_service.create_session()
        return SessionResponse(session_id=session.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}", response_model=SessionHistoryResponse)
async def get_session_history(
    session_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve the conversation history for a session.
    """
    try:
        session_service = SessionService(db)
        history = await session_service.get_session_history(session_id)
        return SessionHistoryResponse(
            session_id=session_id,
            history=history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))