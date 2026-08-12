from typing import Any, Dict, Optional
from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.config.constants import TaskStatus
from app.orchestration.checkpoints import checkpoint_manager
from app.orchestration.events import Event, event_bus
from app.orchestration.state import AgentStepResult, TaskState
from app.utils.logger import logger

class ManagerAgent(BaseAgent):
    name = "manager"
    description = "Master orchestrator managing sub-agents, state transitions, safety policy checks, and workflow execution."
    system_prompt = "You are the ManagerAgent orchestrating specialized AI sub-agents."

    async def run(self, context: AgentContext) -> Dict[str, Any]:
        """Core manager execution method."""
        return {"message": f"Manager initialized for task {context.task_id}"}

    async def execute_step(self, agent: BaseAgent, state: TaskState, next_status: TaskStatus) -> AgentResult:
        """Execute a sub-agent step cleanly through Manager orchestration."""
        state.transition_to(next_status, current_agent=agent.name)
        checkpoint_manager.save_checkpoint(state)

        agent_context = AgentContext(
            task_id=state.task_id,
            user_request=state.user_request,
            repository=state.repository,
            workspace_path=state.workspace_path,
            input_data={
                "plan": state.plan,
                "research_summary": state.research_summary,
                "code_changes": state.code_changes,
                "test_result": state.test_result
            }
        )

        result = await agent.execute(agent_context)

        step_record = AgentStepResult(
            agent_name=agent.name,
            status=result.status,
            summary=result.summary,
            output=result.data,
            errors=result.errors
        )
        state.add_step_result(step_record)
        checkpoint_manager.save_checkpoint(state)

        return result

manager_agent = ManagerAgent()
