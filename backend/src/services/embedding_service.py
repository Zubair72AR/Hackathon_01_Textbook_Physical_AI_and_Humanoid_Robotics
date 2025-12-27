import openai
from typing import List
from ..config import settings
from ..utils import get_logger


class EmbeddingService:
    def __init__(self):
        self.logger = get_logger(__name__)

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI API.
        """
        try:
            openai.api_key = settings.openai_api_key

            # If text is too long, we need to truncate or chunk it
            if len(text) > 8000:  # Approximate limit for OpenAI embedding model
                text = text[:8000]  # Truncate to safe length

            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )

            embedding = response['data'][0]['embedding']
            self.logger.info(f"Generated embedding for text of length {len(text)}")
            return embedding
        except Exception as e:
            self.logger.error(f"Error generating embedding: {str(e)}")
            raise

    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts.
        """
        try:
            openai.api_key = settings.openai_api_key

            # Truncate long texts
            processed_texts = []
            for text in texts:
                if len(text) > 8000:
                    processed_texts.append(text[:8000])
                else:
                    processed_texts.append(text)

            response = openai.Embedding.create(
                input=processed_texts,
                model="text-embedding-ada-002"
            )

            embeddings = [item['embedding'] for item in response['data']]
            self.logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            self.logger.error(f"Error generating embeddings batch: {str(e)}")
            raise