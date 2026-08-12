import asyncio
from typing import Any, Dict
from app.config.constants import PermissionType, RiskLevel
from app.execution.command_runner import command_runner
from app.tools.base import BaseTool

class ShellTool(BaseTool):
    name = "shell"
    description = "Execute authorized shell commands safely inside task workspace."
    permission_type = PermissionType.WRITE
    risk_level = RiskLevel.WRITE_SAFE

    def run(self, command: str, workspace_dir: str, timeout: int = 60) -> Dict[str, Any]:
        """Synchronous runner wrapper calling async command runner."""
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Run in event loop thread pool
            result = asyncio.run_coroutine_threadsafe(
                command_runner.run(command, workspace_dir, timeout), loop
            ).result()
        else:
            result = loop.run_until_complete(
                command_runner.run(command, workspace_dir, timeout)
            )

        return {
            "status": "success" if result.exit_code == 0 else "error",
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration_seconds": result.duration_seconds,
            "timed_out": result.timed_out
        }

shell_tool = ShellTool()
