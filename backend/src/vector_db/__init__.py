from qdrant_client import AsyncQdrantClient
from ..config import settings


# Initialize Qdrant client
qdrant_client = AsyncQdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key,
    prefer_grpc=True
)


async def get_qdrant_client():
    return qdrant_client