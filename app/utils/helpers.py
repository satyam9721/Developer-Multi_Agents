import uuid
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Dict

def generate_id(prefix: str = "id") -> str:
    """Generate unique identifier with prefix."""
    return f"{prefix}-{uuid.uuid4().hex[:10]}"

def get_utc_timestamp() -> str:
    """Return ISO- formatted UTC timestamp string."""
    return datetime.now(timezone.utc).isoformat()

def normalize_path(base_dir: str, target_path: str) -> str:
    """Safely resolve path within a base directory."""
    base = Path(base_dir).resolve()
    target = (base / target_path).resolve()
    return str(target)

def is_path_safe(base_dir: str, target_path: str) -> bool:
    """Check if target_path resides safely within base_dir."""
    base = Path(base_dir).resolve()
    try:
        target = (base / target_path).resolve()
        return base in target.parents or base == target
    except Exception:
        return False

def truncate_text(text: str, max_chars: int = 2000) -> str:
    """Truncate long text string safely."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n... [truncated {len(text) - max_chars} characters]"
