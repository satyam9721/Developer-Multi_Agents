from typing import Any, Dict
from app.agents.base import AgentContext, BaseAgent
from app.services.llm import llm_service
from app.utils.parser import extract_json

class PlannerAgent(BaseAgent):
    name = "planner"
    description = "Decomposes complex task into structured implementation plan and steps."
    system_prompt = "You are the PlannerAgent. Decompose user request into step-by-step implementation DAG."

    async def run(self, context: AgentContext) -> Dict[str, Any]:
        prompt = f"""
Analyze user request: '{context.user_request}'
Repository: '{context.repository}'

Generate structured implementation plan with summary, steps, affected_files, and acceptance_criteria.
"""
        response_text = await llm_service.generate(prompt, system_prompt=self.system_prompt)
        parsed = extract_json(response_text)
        
        if parsed:
            return parsed

        return {
            "summary": f"Plan for {context.user_request}",
            "steps": [
                {"step": 1, "description": "Inspect repository files and structure"},
                {"step": 2, "description": "Implement request logic"},
                {"step": 3, "description": "Verify with unit tests"}
            ],
            "affected_files": [],
            "acceptance_criteria": ["Code compiles and tests pass"]
        }

planner_agent = PlannerAgent()
