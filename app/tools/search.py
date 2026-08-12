import os
import re
from typing import Any, Dict, List
from app.config.constants import PermissionType, RiskLevel
from app.execution.sandbox import sandbox
from app.tools.base import BaseTool

class SearchTool(BaseTool):
    name = "search"
    description = "Search codebase files for string or regex patterns."
    permission_type = PermissionType.READ
    risk_level = RiskLevel.READ_ONLY

    def run(self, query: str, workspace_dir: str, file_pattern: str = "*") -> Dict[str, Any]:
        """Search codebase for matching text or regex pattern."""
        target_dir = sandbox.validate_path(workspace_dir, ".")
        results = []

        try:
            regex = re.compile(query, re.IGNORECASE)
        except re.error:
            regex = re.compile(re.escape(query), re.IGNORECASE)

        for root, _, files in os.walk(target_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), target_dir)
                if file.startswith(".") or "node_modules" in rel_path or "venv" in rel_path:
                    continue

                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line_num, line in enumerate(f, 1):
                            if regex.search(line):
                                results.append({
                                    "file": rel_path,
                                    "line_number": line_num,
                                    "content": line.strip()
                                })
                                if len(results) >= 100:
                                    break
                except Exception:
                    continue

        return {"status": "success", "total_matches": len(results), "matches": results}

search_tool = SearchTool()
