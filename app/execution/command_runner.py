import asyncio
import time
from typing import Dict, Optional
from pydantic import BaseModel, Field
from app.policies.command_policy import CommandPolicy
from app.utils.logger import logger

class CommandResult(BaseModel):
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_seconds: float
    timed_out: bool = False

class CommandRunner:
    """Executes safe shell commands within workspace boundaries."""

    @staticmethod
    async def run(
        command: str,
        cwd: str,
        timeout: int = 60,
        env: Optional[Dict[str, str]] = None
    ) -> CommandResult:
        """Run command asynchronously with timeout, policy checks, and output capture."""
        # Enforce command policy check
        CommandPolicy.validate_command(command)

        start_time = time.time()
        logger.info(f"Executing command: '{command}' in cwd: '{cwd}'")

        try:
            process = await asyncio.create_subprocess_shell(
                command,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    process.communicate(), timeout=float(timeout)
                )
                duration = time.time() - start_time
                stdout = stdout_bytes.decode("utf-8", errors="replace")
                stderr = stderr_bytes.decode("utf-8", errors="replace")
                exit_code = process.returncode if process.returncode is not None else -1

                return CommandResult(
                    command=command,
                    exit_code=exit_code,
                    stdout=stdout,
                    stderr=stderr,
                    duration_seconds=round(duration, 3),
                    timed_out=False
                )

            except asyncio.TimeoutError:
                process.kill()
                duration = time.time() - start_time
                logger.error(f"Command timed out after {timeout}s: '{command}'")
                return CommandResult(
                    command=command,
                    exit_code=-1,
                    stdout="",
                    stderr=f"Command timed out after {timeout} seconds",
                    duration_seconds=round(duration, 3),
                    timed_out=True
                )

        except Exception as exc:
            duration = time.time() - start_time
            logger.error(f"Failed to execute command '{command}': {exc}")
            return CommandResult(
                command=command,
                exit_code=-1,
                stdout="",
                stderr=str(exc),
                duration_seconds=round(duration, 3),
                timed_out=False
            )

command_runner = CommandRunner()
