import os
from typing import Any, Dict, List, Optional
from app.config.constants import PermissionType, RiskLevel
from app.execution.sandbox import sandbox
from app.tools.base import BaseTool
from app.utils.parser import parse_diff_summary

class FilesystemTool(BaseTool):
    name = "filesystem"
    description = "Read, write, edit, list, and diff files inside task workspace sandbox."
    permission_type = PermissionType.WRITE
    risk_level = RiskLevel.WRITE_SAFE

    def run(self, action: str, workspace_dir: str, file_path: str = "", content: str = "", target_content: str = "", replacement_content: str = "") -> Dict[str, Any]:
        """Execute filesystem operations with sandbox enforcement."""
        if action == "read":
            target = sandbox.validate_path(workspace_dir, file_path)
            if not target.exists():
                return {"status": "error", "error": f"File '{file_path}' does not exist."}
            with open(target, "r", encoding="utf-8") as f:
                data = f.read()
            return {"status": "success", "content": data}

        elif action == "write":
            target = sandbox.validate_path(workspace_dir, file_path)
            os.makedirs(target.parent, exist_ok=True)
            with open(target, "w", encoding="utf-8") as f:
                f.write(content)
            return {"status": "success", "file_path": file_path, "bytes_written": len(content)}

        elif action == "edit":
            target = sandbox.validate_path(workspace_dir, file_path)
            if not target.exists():
                return {"status": "error", "error": f"File '{file_path}' does not exist for editing."}
            with open(target, "r", encoding="utf-8") as f:
                original = f.read()
            if target_content not in original:
                return {"status": "error", "error": "target_content not found in file."}
            updated = original.replace(target_content, replacement_content, 1)
            with open(target, "w", encoding="utf-8") as f:
                f.write(updated)
            return {"status": "success", "file_path": file_path}

        elif action == "list":
            target = sandbox.validate_path(workspace_dir, file_path or ".")
            if not target.exists() or not target.is_dir():
                return {"status": "error", "error": f"Directory '{file_path}' does not exist."}
            files = [str(p.relative_to(target)) for p in target.glob("**/*") if p.is_file()]
            return {"status": "success", "files": files}

        else:
            return {"status": "error", "error": f"Unsupported filesystem action '{action}'"}

filesystem_tool = FilesystemTool()
