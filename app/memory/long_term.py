from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.utils.helpers import generate_id, get_utc_timestamp

class MemoryRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: generate_id("mem"))
    repository: str
    category: str  # fix_pattern, repository_knowledge, known_failure
    content: Dict[str, Any]
    created_at: str = Field(default_factory=get_utc_timestamp)

class LongTermMemory:
    """Repository-scoped long-term memory store."""

    def __init__(self):
        self._store: Dict[str, List[MemoryRecord]] = {}

    def save_knowledge(self, repository: str, category: str, content: Dict[str, Any]) -> MemoryRecord:
        """Store knowledge snippet scoped to repository."""
        if repository not in self._store:
            self._store[repository] = []

        record = MemoryRecord(repository=repository, category=category, content=content)
        self._store[repository].append(record)
        return record

    def query_knowledge(self, repository: str, category: Optional[str] = None) -> List[MemoryRecord]:
        """Retrieve repository-scoped knowledge entries."""
        records = self._store.get(repository, [])
        if category:
            return [r for r in records if r.category == category]
        return records

long_term_memory = LongTermMemory()
