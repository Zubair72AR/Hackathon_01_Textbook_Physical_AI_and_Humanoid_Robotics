from fastapi import FastAPI
from .v1 import router as v1_router


def create_app() -> FastAPI:
    app = FastAPI(title="Unified AI Book RAG Chatbot API")

    # Include API routers
    app.include_router(v1_router, prefix="/api/v1", tags=["v1"])

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "timestamp": "2025-12-25"}

    return app