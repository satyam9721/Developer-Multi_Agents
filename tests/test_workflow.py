import pytest
from app.config.constants import TaskStatus
from app.workflows.software import software_workflow

@pytest.mark.asyncio
async def test_software_development_workflow():
    state = await software_workflow.execute(
        user_request="Fix farmer API bug",
        repository="myorg/farmer-service"
    )
    assert state.task_id is not None
    assert state.status in [TaskStatus.READY_FOR_PR, TaskStatus.READY_FOR_REVIEW]
    assert len(state.steps) >= 5
