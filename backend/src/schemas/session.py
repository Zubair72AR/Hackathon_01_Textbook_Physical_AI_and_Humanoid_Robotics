from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from datetime import datetime


class SessionResponse(BaseModel):
    session_id: UUID


class QueryHistoryItem(BaseModel):
    query: str
    response: str
    timestamp: datetime


class SessionHistoryResponse(BaseModel):
    session_id: UUID
    history: List[QueryHistoryItem]