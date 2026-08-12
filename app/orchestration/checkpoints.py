import json
import os
from typing import Dict, Optional
from app.orchestration.state import TaskState
from app.utils.logger import logger

class CheckpointManager:
    """Manages persistence of TaskState checkpoints."""
    def __init__(self, storage_dir: str = "./checkpoints"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self._memory_cache: Dict[str, TaskState] = {}

    def save_checkpoint(self, state: TaskState) -> bool:
        """Save state to in-memory cache and local file disk."""
        try:
            self._memory_cache[state.task_id] = state
            file_path = os.path.join(self.storage_dir, f"{state.task_id}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(state.model_dump_json(indent=2))
            logger.info(f"Saved checkpoint for task {state.task_id}")
            return True
        except Exception as exc:
            logger.error(f"Failed to save checkpoint for task {state.task_id}: {exc}")
            return False

    def load_checkpoint(self, task_id: str) -> Optional[TaskState]:
        """Load state from memory cache or file disk."""
        if task_id in self._memory_cache:
            return self._memory_cache[task_id]

        file_path = os.path.join(self.storage_dir, f"{task_id}.json")
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            state = TaskState(**data)
            self._memory_cache[task_id] = state
            return state
        except Exception as exc:
            logger.error(f"Failed to load checkpoint for task {task_id}: {exc}")
            return None

checkpoint_manager = CheckpointManager()
