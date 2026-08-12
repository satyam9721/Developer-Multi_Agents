from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.base import AgentContext
from app.agents.planner import planner_agent
from app.agents.coder import coder_agent
from app.agents.reviewer import reviewer_agent
from app.agents.tester import tester_agent
from app.agents.researcher import researcher_agent
from app.execution.environment import workspace_manager

router = APIRouter(prefix="/api/agents", tags=["Agents"])

class AgentRunRequest(BaseModel):
    agent_name: str
    user_request: str
    repository: str

AGENTS_MAP = {
    "planner": planner_agent,
    "researcher": researcher_agent,
    "coder": coder_agent,
    "reviewer": reviewer_agent,
    "tester": tester_agent,
}

@router.post("/run")
async def run_agent(req: AgentRunRequest):
    """Directly execute a specialized agent."""
    agent = AGENTS_MAP.get(req.agent_name.lower())
    if not agent:
        raise HTTPException(status_code=400, detail=f"Agent '{req.agent_name}' not found.")

    workspace_dir = workspace_manager.get_task_workspace("direct-run")
    context = AgentContext(
        task_id="direct-run",
        user_request=req.user_request,
        repository=req.repository,
        workspace_path=str(workspace_dir)
    )

    result = await agent.execute(context)
    return result.model_dump()
