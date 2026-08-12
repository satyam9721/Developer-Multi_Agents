import asyncio
from typing import Dict, Optional
from app.utils.logger import logger

class ProcessManager:
    """Manages long-running background processes (e.g. dev servers, proxies)."""

    def __init__(self):
        self._processes: Dict[str, asyncio.subprocess.Process] = {}

    def register_process(self, name: str, process: asyncio.subprocess.Process) -> None:
        """Register process handle."""
        self._processes[name] = process
        logger.info(f"Registered process '{name}' (PID: {process.pid})")

    async def stop_process(self, name: str) -> bool:
        """Terminate a running process."""
        if name in self._processes:
            proc = self._processes.pop(name)
            try:
                proc.terminate()
                await proc.wait()
                logger.info(f"Stopped process '{name}'")
                return True
            except Exception as exc:
                logger.error(f"Error stopping process '{name}': {exc}")
                return False
        return False

    async def stop_all(self) -> None:
        """Terminate all registered processes on shutdown."""
        for name in list(self._processes.keys()):
            await self.stop_process(name)

process_manager = ProcessManager()
