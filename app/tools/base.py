from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel
from app.config.constants import PermissionType, RiskLevel
from app.policies.permissions import PermissionChecker
from app.utils.logger import logger

class BaseTool(ABC):
    """Abstract base class for all operational tools."""

    name: str
    description: str
    permission_type: PermissionType = PermissionType.READ
    risk_level: RiskLevel = RiskLevel.READ_ONLY

    def execute_with_policy(self, agent_role: str, **kwargs) -> Dict[str, Any]:
        """Validate security policies before executing tool."""
        PermissionChecker.check_permission(agent_role, self.permission_type, self.risk_level)
        logger.info(f"Executing tool '{self.name}' requested by agent '{agent_role}'")
        return self.run(**kwargs)

    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        """Core tool logic implementation."""
        pass
