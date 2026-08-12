from typing import Any, Dict
from app.agents.base import AgentContext, BaseAgent
from app.tools.filesystem import filesystem_tool
from app.tools.search import search_tool

class ResearcherAgent(BaseAgent):
    name = "researcher"
    description = "Explores repository structure, searches code, and synthesizes findings without modifying source code."
    system_prompt = "You are the ResearcherAgent. Gather information about codebase, APIs, and dependencies."

    async def run(self, context: AgentContext) -> Dict[str, Any]:
        # Search workspace directory contents
        files_result = filesystem_tool.execute_with_policy(
            agent_role=self.name,
            action="list",
            workspace_dir=context.workspace_path
        )

        return {
            "summary": f"Researched codebase for {context.user_request}",
            "workspace_files": files_result.get("files", []),
            "relevant_symbols": [],
            "dependencies": []
        }

researcher_agent = ResearcherAgent()
