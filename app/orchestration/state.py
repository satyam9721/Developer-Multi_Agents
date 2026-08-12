from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.config.constants import TaskStatus
from app.utils.helpers import generate_id, get_utc_timestamp

class AgentStepResult(BaseModel):
    step_id: str = Field(default_factory=lambda: generate_id("step"))
    agent_name: str
    status: str  # SUCCESS, FAILED, SKIPPED
    summary: str
    output: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=get_utc_timestamp)

class TaskState(BaseModel):
    task_id: str = Field(default_factory=lambda: generate_id("task"))
    user_request: str
    repository: str
    workspace_path: str
    status: TaskStatus = TaskStatus.CREATED
    current_agent: Optional[str] = None
    
    plan: Dict[str, Any] = Field(default_factory=dict)
    research_summary: Dict[str, Any] = Field(default_factory=dict)
    code_changes: List[Dict[str, Any]] = Field(default_factory=list)
    diff_summary: Dict[str, Any] = Field(default_factory=dict)
    review_result: Dict[str, Any] = Field(default_factory=dict)
    test_result: Dict[str, Any] = Field(default_factory=dict)
    
    branch_name: Optional[str] = None
    pr_url: Optional[str] = None
    deployment_url: Optional[str] = None

    steps: List[AgentStepResult] = Field(default_factory=list)
    artifacts: Dict[str, str] = Field(default_factory=dict)
    requires_approval: bool = False
    approval_reason: Optional[str] = None

    created_at: str = Field(default_factory=get_utc_timestamp)
    updated_at: str = Field(default_factory=get_utc_timestamp)

    def transition_to(self, new_status: TaskStatus, current_agent: Optional[str] = None) -> None:
        """Update task status safely."""
        self.status = new_status
        if current_agent is not None:
            self.current_agent = current_agent
        self.updated_at = get_utc_timestamp()

    def add_step_result(self, step_result: AgentStepResult) -> None:
        """Append an agent execution result."""
        self.steps.append(step_result)
        self.updated_at = get_utc_timestamp()
