from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from typing import List, Optional
from ..models import UserSession, Query
from ..utils import get_logger


class SessionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.logger = get_logger(__name__)

    async def create_session(self) -> UserSession:
        """Create a new user session."""
        try:
            # Session expires in 24 hours
            expires_at = datetime.now() + timedelta(hours=24)

            session = UserSession(
                id=uuid4(),
                expires_at=expires_at
            )

            self.db.add(session)
            await self.db.commit()
            await self.db.refresh(session)

            self.logger.info(f"Created new session: {session.id}")
            return session
        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"Error creating session: {str(e)}")
            raise

    async def get_session(self, session_id: UUID) -> Optional[UserSession]:
        """Get a user session by ID."""
        try:
            result = await self.db.execute(
                select(UserSession).where(UserSession.id == session_id)
            )
            session = result.scalar_one_or_none()

            if session and session.is_expired():
                await self.db.delete(session)
                await self.db.commit()
                return None

            return session
        except Exception as e:
            self.logger.error(f"Error getting session {session_id}: {str(e)}")
            raise

    async def get_session_history(self, session_id: UUID) -> List[dict]:
        """Get the conversation history for a session."""
        try:
            # First, check if session exists and is not expired
            session = await self.get_session(session_id)
            if not session:
                raise ValueError(f"Session {session_id} not found or expired")

            # Get all queries for this session
            result = await self.db.execute(
                select(Query)
                .where(Query.session_id == session_id)
                .order_by(Query.created_at)
            )
            queries = result.scalars().all()

            history = []
            for query in queries:
                history.append({
                    "query": query.query_text,
                    "response": query.response_text,
                    "timestamp": query.created_at
                })

            return history
        except Exception as e:
            self.logger.error(f"Error getting session history {session_id}: {str(e)}")
            raise