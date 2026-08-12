import pytest
from app.agents.base import AgentContext
from app.agents.planner import planner_agent
from app.agents.researcher import researcher_agent

@pytest.mark.asyncio
async def test_planner_agent_run(tmp_path):
    context = AgentContext(
        task_id="test-1",
        user_request="Fix farmer API bug",
        repository="org/repo",
        workspace_path=str(tmp_path)
    )
    result = await planner_agent.execute(context)
    assert result.status == "SUCCESS"
    assert "summary" in result.data
    assert "steps" in result.data

@pytest.mark.asyncio
async def test_researcher_agent_run(tmp_path):
    context = AgentContext(
        task_id="test-2",
        user_request="Find farmer controller",
        repository="org/repo",
        workspace_path=str(tmp_path)
    )
    result = await researcher_agent.execute(context)
    assert result.status == "SUCCESS"
    assert "workspace_files" in result.data
