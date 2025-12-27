from sqlalchemy import Column, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from .base import Base
import uuid


class Query(Base):
    __tablename__ = "queries"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(PostgresUUID(as_uuid=True), ForeignKey("user_sessions.id"), nullable=False)
    query_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    sources = Column(JSON)  # Store as JSON array of source references

    # Relationships
    session = relationship("UserSession")