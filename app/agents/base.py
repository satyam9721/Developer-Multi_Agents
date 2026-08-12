from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.utils.helpers import generate_id, get_utc_timestamp
from app.utils.logger import logger

class AgentContext(BaseModel):
    task_id: str
    user_request: str
    repository: str
    workspace_path: str
    input_data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentResult(BaseModel):
    agent_name: str
    status: str  # SUCCESS, FAILED, SKIPPED
    summary: str
    data: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=get_utc_timestamp)

class BaseAgent(ABC):
    """Abstract Base Class for all specialized AI Agents."""

    name: str
    description: str
    system_prompt: str

    async def execute(self, context: AgentContext) -> AgentResult:
        """Standardized execution wrapper with logging and error handling."""
        logger.info(f"Starting agent '{self.name}' for task '{context.task_id}'")
        try:
            result_data = await self.run(context)
            logger.info(f"Agent '{self.name}' completed successfully.")
            return AgentResult(
                agent_name=self.name,
                status="SUCCESS",
                summary=f"Agent {self.name} completed successfully.",
                data=result_data,
                errors=[]
            )
        except Exception as exc:
            logger.error(f"Agent '{self.name}' failed on task '{context.task_id}': {exc}")
            return AgentResult(
                agent_name=self.name,
                status="FAILED",
                summary=f"Agent {self.name} failed.",
                data={},
                errors=[str(exc)]
            )

    @abstractmethod
    async def run(self, context: AgentContext) -> Dict[str, Any]:
        """Core agent execution logic."""
        pass
