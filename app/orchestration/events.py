from typing import Any, Callable, Dict, List
import asyncio
from pydantic import BaseModel, Field
from app.config.constants import EventTypes
from app.utils.helpers import generate_id, get_utc_timestamp
from app.utils.logger import logger

class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: generate_id("event"))
    event_type: EventTypes
    task_id: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=get_utc_timestamp)

EventHandler = Callable[[Event], None]

class EventBus:
    """Async in-memory EventBus for decoupled state notification."""
    def __init__(self):
        self._subscribers: Dict[EventTypes, List[EventHandler]] = {}

    def subscribe(self, event_type: EventTypes, handler: EventHandler) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish(self, event: Event) -> None:
        logger.info(f"Event published: {event.event_type} for task {event.task_id}")
        handlers = self._subscribers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as exc:
                logger.error(f"Error in event handler for {event.event_type}: {exc}")

event_bus = EventBus()
