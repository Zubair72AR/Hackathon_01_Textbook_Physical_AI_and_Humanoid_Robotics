from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from .base import Base
import uuid


class Section(Base):
    __tablename__ = "sections"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(PostgresUUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False)
    word_count = Column(Integer, default=0)

    # Relationships
    chapter = relationship("Chapter", back_populates="sections")
    contents = relationship("BookContent", back_populates="section")