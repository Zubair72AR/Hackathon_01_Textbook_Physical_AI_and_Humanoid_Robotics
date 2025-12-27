from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from .base import Base
import uuid


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(PostgresUUID(as_uuid=True), ForeignKey("book_content.id"), nullable=False)
    vector = Column(JSON, nullable=False)  # Store embedding as JSON array
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False, default=0)

    # Relationships
    content = relationship("BookContent", back_populates="embeddings")