from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.utils.helpers import generate_id, get_utc_timestamp

class Message(BaseModel):
    message_id: str = Field(default_factory=lambda: generate_id("msg"))
    role: str  # user, assistant, system
    content: str
    timestamp: str = Field(default_factory=get_utc_timestamp)

class ConversationMemory:
    """Manages chat turn history and token budget truncation."""

    def __init__(self, task_id: str, max_messages: int = 50):
        self.task_id = task_id
        self.max_messages = max_messages
        self.history: List[Message] = []

    def add_message(self, role: str, content: str) -> Message:
        """Add user or assistant turn message."""
        msg = Message(role=role, content=content)
        self.history.append(msg)
        if len(self.history) > self.max_messages:
            self.history.pop(0)
        return msg

    def get_formatted_history(self) -> List[Dict[str, str]]:
        """Return history formatted for LLM prompts."""
        return [{"role": m.role, "content": m.content} for m in self.history]
