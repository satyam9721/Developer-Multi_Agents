from typing import Any, Dict, List
from app.utils.logger import logger

class VectorService:
    """Vector database client abstraction wrapper."""

    def __init__(self):
        self._mock_index: Dict[str, List[Dict[str, Any]]] = {}

    async def upsert(self, collection_name: str, document_id: str, vector: List[float], metadata: Dict[str, Any]) -> bool:
        """Upsert document vector into collection."""
        if collection_name not in self._mock_index:
            self._mock_index[collection_name] = []
        self._mock_index[collection_name].append({
            "id": document_id,
            "vector": vector,
            "metadata": metadata
        })
        logger.info(f"Upserted vector document '{document_id}' in collection '{collection_name}'")
        return True

    async def search(self, collection_name: str, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search vector database collection."""
        items = self._mock_index.get(collection_name, [])
        return items[:limit]

vector_service = VectorService()
