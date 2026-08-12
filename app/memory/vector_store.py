from typing import Any, Dict, List
from app.services.embedding import embedding_service
from app.services.vector import vector_service
from app.utils.logger import logger

class VectorStore:
    """Semantic vector store index for repository code & documentation."""

    async def index_file(self, repository: str, file_path: str, content: str) -> bool:
        """Index a file's content into vector store."""
        embedding = await embedding_service.get_embedding(content)
        doc_id = f"{repository}:{file_path}"
        metadata = {"repository": repository, "file_path": file_path, "content_snippet": content[:300]}
        await vector_service.upsert(repository, doc_id, embedding, metadata)
        logger.info(f"Indexed file '{file_path}' into vector store for repository '{repository}'")
        return True

    async def search_similar_code(self, repository: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search codebase semantically for code relevant to query."""
        query_embedding = await embedding_service.get_embedding(query)
        results = await vector_service.search(repository, query_embedding, limit=limit)
        return results

vector_store = VectorStore()
