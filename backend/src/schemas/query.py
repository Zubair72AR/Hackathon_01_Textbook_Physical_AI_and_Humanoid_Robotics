from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID


class SourceReference(BaseModel):
    content_id: UUID
    title: str
    relevance_score: float
    text_preview: str


class QueryResponse(BaseModel):
    response: str
    sources: List[SourceReference]
    session_id: UUID


class QueryRequest(BaseModel):
    query: str
    session_id: Optional[UUID] = None
    context_selection: Optional[str] = None
    max_tokens: Optional[int] = 500
    context_content_ids: Optional[List[UUID]] = None