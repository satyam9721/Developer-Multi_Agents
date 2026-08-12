from typing import Any, Dict
from app.config.constants import PermissionType, RiskLevel
from app.policies.permissions import PolicyViolationError
from app.tools.base import BaseTool

class DatabaseTool(BaseTool):
    name = "database"
    description = "Inspect database schema and execute safe read queries."
    permission_type = PermissionType.HIGH_RISK
    risk_level = RiskLevel.HIGH_RISK

    def run(self, action: str, query: str = "") -> Dict[str, Any]:
        """Execute database query or schema inspection."""
        clean_query = query.strip().upper()
        if any(keyword in clean_query for keyword in ["DROP", "TRUNCATE", "ALTER", "DELETE"]):
            raise PolicyViolationError("Destructive database operations are blocked by DatabaseTool policy.")

        if action == "inspect_schema":
            return {
                "status": "success",
                "tables": ["users", "repositories", "tasks", "task_events", "agent_runs", "memory_records"]
            }
        elif action == "query":
            return {
                "status": "success",
                "query": query,
                "rows_affected": 0,
                "data": []
            }
        
        return {"status": "error", "error": f"Unsupported database action '{action}'"}

database_tool = DatabaseTool()
