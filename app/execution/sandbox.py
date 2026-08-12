from pathlib import Path
from app.policies.permissions import PolicyViolationError
from app.utils.helpers import is_path_safe

class SandboxValidator:
    """Validates that file operations stay strictly inside the authorized task workspace."""

    @staticmethod
    def validate_path(workspace_dir: str, target_path: str) -> Path:
        """Resolve and validate target path within workspace boundary."""
        if not is_path_safe(workspace_dir, target_path):
            raise PolicyViolationError(
                f"Path traversal blocked: '{target_path}' is outside authorized workspace '{workspace_dir}'"
            )
        resolved = (Path(workspace_dir) / target_path).resolve()
        return resolved

sandbox = SandboxValidator()
