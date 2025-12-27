from fastapi import APIRouter
from . import query, sessions, ingest


router = APIRouter()

# Include API endpoints
router.include_router(query.router, tags=["query"])
router.include_router(sessions.router, tags=["sessions"])
router.include_router(ingest.router, tags=["ingest"])