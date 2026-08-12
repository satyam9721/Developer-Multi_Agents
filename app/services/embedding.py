from typing import List
from app.utils.logger import logger

class EmbeddingService:
    """Service abstraction for generating text vector embeddings."""

    async def get_embedding(self, text: str) -> List[float]:
        """Generate vector embedding for text string."""
        # Mock 128-dimensional embedding vector for fallback
        logger.info(f"Generating embedding for text length {len(text)}")
        return [0.1] * 128

embedding_service = EmbeddingService()
