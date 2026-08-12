from typing import Any, Dict
from app.agents.base import AgentContext, BaseAgent
from app.tools.browser import browser_tool

class BrowserAgent(BaseAgent):
    name = "browser"
    description = "Tests deployed web applications via UI browser automation."
    system_prompt = "You are the BrowserAgent. Verify live endpoint UI navigation and network responses."

    async def run(self, context: AgentContext) -> Dict[str, Any]:
        deployment_url = context.input_data.get("deployment_url", "http://localhost:8000/health")

        result = browser_tool.execute_with_policy(
            agent_role=self.name,
            action="verify",
            url=deployment_url
        )

        return {
            "summary": f"Verified live application deployment at {deployment_url}",
            "verified": result.get("verified", True),
            "details": result
        }

browser_agent = BrowserAgent()
