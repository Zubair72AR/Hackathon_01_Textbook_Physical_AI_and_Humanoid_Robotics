from sqlalchemy import Column, Integer, String, Text, ForeignKey, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from .base import Base
import uuid


class BookContent(Base):
    __tablename__ = "book_content"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module_id = Column(PostgresUUID(as_uuid=True), ForeignKey("modules.id"), nullable=False)
    chapter_id = Column(PostgresUUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False)
    section_id = Column(PostgresUUID(as_uuid=True), ForeignKey("sections.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    word_count = Column(Integer, default=0)
    version = Column(Integer, default=1)

    # Relationships
    module = relationship("Module", back_populates="contents")
    chapter = relationship("Chapter", back_populates="contents")
    section = relationship("Section", back_populates="contents")
    embeddings = relationship("Embedding", back_populates="content", cascade="all, delete-orphan")