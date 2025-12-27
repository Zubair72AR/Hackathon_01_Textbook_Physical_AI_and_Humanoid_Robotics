from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from .base import Base
import uuid
from datetime import datetime


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PostgresUUID(as_uuid=True))  # Optional, for authenticated users
    expires_at = Column(DateTime(timezone=True))

    def is_expired(self):
        if self.expires_at:
            return datetime.now(self.expires_at.tzinfo) > self.expires_at
        return False