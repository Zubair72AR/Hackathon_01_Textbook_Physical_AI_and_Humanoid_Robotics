from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from .base import Base
import uuid


class Module(Base):
    __tablename__ = "modules"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False, unique=True)

    # Relationships
    chapters = relationship("Chapter", back_populates="module", cascade="all, delete-orphan")
    contents = relationship("BookContent", back_populates="module")