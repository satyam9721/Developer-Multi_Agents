import os
import shutil
from pathlib import Path
from app.config.settings import settings
from app.utils.logger import logger

class WorkspaceManager:
    """Manages creation, resolution, and isolation of per-task workspace repositories."""

    def __init__(self, root_dir: str = settings.WORKSPACE_ROOT):
        self.root_dir = Path(root_dir).resolve()
        os.makedirs(self.root_dir, exist_ok=True)

    def get_task_workspace(self, task_id: str) -> Path:
        """Return task-isolated workspace path."""
        task_dir = (self.root_dir / f"task-{task_id}" / "repository").resolve()
        os.makedirs(task_dir, exist_ok=True)
        return task_dir

    def cleanup_workspace(self, task_id: str) -> bool:
        """Remove task workspace directory."""
        task_dir = self.root_dir / f"task-{task_id}"
        if task_dir.exists():
            try:
                shutil.rmtree(task_dir)
                logger.info(f"Cleaned up workspace for task {task_id}")
                return True
            except Exception as exc:
                logger.error(f"Failed to cleanup workspace for task {task_id}: {exc}")
                return False
        return True

workspace_manager = WorkspaceManager()
