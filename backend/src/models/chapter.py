from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from .base import Base
import uuid


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module_id = Column(PostgresUUID(as_uuid=True), ForeignKey("modules.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False)
    word_count = Column(Integer, default=0)

    # Relationships
    module = relationship("Module", back_populates="chapters")
    sections = relationship("Section", back_populates="chapter", cascade="all, delete-orphan")
    contents = relationship("BookContent", back_populates="chapter")