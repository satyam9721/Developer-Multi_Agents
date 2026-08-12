from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config.constants import TaskStatus
from app.execution.environment import workspace_manager
from app.orchestration.checkpoints import checkpoint_manager
from app.orchestration.state import TaskState
from app.workflows.software import software_workflow

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

class TaskCreateRequest(BaseModel):
    repository: str
    task: str

class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    repository: str
    user_request: str

@router.post("", response_model=TaskResponse)
async def create_task(req: TaskCreateRequest):
    """Create a new autonomous task and trigger SoftwareDevelopmentWorkflow."""
    state = TaskState(user_request=req.task, repository=req.repository, workspace_path="")
    workspace_dir = workspace_manager.get_task_workspace(state.task_id)
    state.workspace_path = str(workspace_dir)
    checkpoint_manager.save_checkpoint(state)

    # Run workflow execution asynchronously
    await software_workflow.execute(req.task, req.repository)

    latest_state = checkpoint_manager.load_checkpoint(state.task_id) or state

    return TaskResponse(
        task_id=latest_state.task_id,
        status=latest_state.status,
        repository=latest_state.repository,
        user_request=latest_state.user_request
    )

@router.get("/{task_id}")
async def get_task(task_id: str):
    """Retrieve state checkpoint for a specific task."""
    state = checkpoint_manager.load_checkpoint(task_id)
    if not state:
        raise HTTPException(status_code=404, detail="Task not found")
    return state.model_dump()
