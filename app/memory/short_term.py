from typing import Any, Dict, List, Optional

class ShortTermMemory:
    """Task-scoped working memory context buffer."""

    def __init__(self, task_id: str):
        self.task_id = task_id
        self._context: Dict[str, Any] = {}
        self._scratchpad: List[str] = []

    def set(self, key: str, value: Any) -> None:
        """Store key-value in short-term context."""
        self._context[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve key from context."""
        return self._context.get(key, default)

    def add_scratchpad_note(self, note: str) -> None:
        """Append thought or intermediate observation to scratchpad."""
        self._scratchpad.append(note)

    def get_scratchpad(self) -> List[str]:
        """Get scratchpad history."""
        return self._scratchpad

    def clear(self) -> None:
        """Clear short term memory."""
        self._context.clear()
        self._scratchpad.clear()
