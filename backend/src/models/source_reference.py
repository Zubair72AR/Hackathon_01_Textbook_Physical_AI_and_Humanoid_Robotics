from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from .base import Base
import uuid


class SourceReference(Base):
    __tablename__ = "source_references"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(PostgresUUID(as_uuid=True), ForeignKey("book_content.id"), nullable=False)
    start_char = Column(Integer, nullable=False)
    end_char = Column(Integer, nullable=False)
    confidence_score = Column(Float, default=0.0)  # 0.0 to 1.0

    # Relationships
    content = relationship("BookContent")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate that start_char is less than end_char
        if 'start_char' in kwargs and 'end_char' in kwargs:
            if kwargs['start_char'] >= kwargs['end_char']:
                raise ValueError("start_char must be less than end_char")