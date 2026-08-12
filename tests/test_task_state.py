import pytest
from app.config.constants import TaskStatus
from app.orchestration.state import TaskState, AgentStepResult

def test_task_state_creation_and_transition():
    state = TaskState(user_request="Fix farmer API bug", repository="myorg/farmer-service", workspace_path="/tmp/workspace")
    assert state.status == TaskStatus.CREATED
    assert state.user_request == "Fix farmer API bug"

    state.transition_to(TaskStatus.PLANNING, current_agent="planner")
    assert state.status == TaskStatus.PLANNING
    assert state.current_agent == "planner"

def test_task_state_add_step():
    state = TaskState(user_request="Refactor auth router", repository="myorg/auth-service", workspace_path="/tmp/workspace")
    step = AgentStepResult(agent_name="planner", status="SUCCESS", summary="Planned steps", output={"steps": [1, 2]})
    state.add_step_result(step)
    assert len(state.steps) == 1
    assert state.steps[0].agent_name == "planner"
