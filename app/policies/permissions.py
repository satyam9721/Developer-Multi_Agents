from typing import List
from app.config.constants import PermissionType, RiskLevel
from app.utils.logger import logger

class PolicyViolationError(Exception):
    """Custom exception raised when a security policy is violated."""
    pass

class PermissionChecker:
    """Validates if requested agent/tool operation adheres to security policies."""
    
    @staticmethod
    def check_permission(agent_role: str, action_type: PermissionType, risk_level: RiskLevel) -> bool:
        """Verify whether an action is permitted for the given agent role."""
        if risk_level == RiskLevel.DESTRUCTIVE:
            logger.warning(f"BLOCKED: Action by agent '{agent_role}' rejected as DESTRUCTIVE.")
            raise PolicyViolationError(f"Action by agent '{agent_role}' rejected: DESTRUCTIVE operations are disallowed.")

        if action_type == PermissionType.HIGH_RISK and risk_level == RiskLevel.HIGH_RISK:
            if agent_role not in ["manager", "reviewer"]:
                logger.warning(f"BLOCKED: Agent '{agent_role}' attempted HIGH_RISK operation without manager approval.")
                raise PolicyViolationError(f"Agent '{agent_role}' is not authorized to execute HIGH_RISK operations.")

        return True
