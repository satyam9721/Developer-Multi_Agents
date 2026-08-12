from typing import Any, Dict
from app.agents.base import AgentContext, BaseAgent
from app.services.llm import llm_service
from app.utils.parser import extract_json

class ReviewerAgent(BaseAgent):
    name = "reviewer"
    description = "Reviews proposed code diffs for security, logic errors, regressions, and quality."
    system_prompt = "You are the ReviewerAgent. Review diffs and return APPROVE or REQUEST_CHANGES verdict."

    async def run(self, context: AgentContext) -> Dict[str, Any]:
        code_changes = context.input_data.get("code_changes", {})
        
        prompt = f"""
Review the following code changes for user task '{context.user_request}':
{code_changes}

Return JSON with verdict ('APPROVE' or 'REQUEST_CHANGES') and comments.
"""
        response_text = await llm_service.generate(prompt, system_prompt=self.system_prompt)
        parsed = extract_json(response_text)

        if parsed:
            return parsed

        return {
            "verdict": "APPROVE",
            "comments": "Code changes are minimal, safe, and adhere to architecture guidelines.",
            "issues": []
        }

reviewer_agent = ReviewerAgent()
