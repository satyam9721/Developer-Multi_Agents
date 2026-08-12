from typing import Any, Dict
from app.agents.manager import manager_agent
from app.agents.tester import tester_agent
from app.config.constants import TaskStatus
from app.execution.environment import workspace_manager
from app.orchestration.state import TaskState

class QAWorkflow:
    """Automated Quality Assurance & Testing Workflow."""

    async def execute(self, user_request: str, repository: str) -> TaskState:
        state = TaskState(user_request=user_request, repository=repository, workspace_path="")
        workspace_dir = workspace_manager.get_task_workspace(state.task_id)
        state.workspace_path = str(workspace_dir)

        res = await manager_agent.execute_step(tester_agent, state, TaskStatus.TESTING)
        state.test_result = res.data
        state.transition_to(TaskStatus.COMPLETED, current_agent="manager")
        return state

qa_workflow = QAWorkflow()
