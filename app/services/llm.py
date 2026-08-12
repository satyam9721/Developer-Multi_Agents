from typing import Any, Dict, Optional
import json
from app.config.settings import settings
from app.utils.logger import logger

class LLMService:
    """Unified abstraction layer for LLM providers with safe mock fallback."""

    def __init__(self, provider: str = settings.LLM_PROVIDER, model: str = settings.LLM_MODEL, api_key: Optional[str] = settings.LLM_API_KEY):
        self.provider = provider
        self.model = model
        self.api_key = api_key

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text completion from configured LLM provider or mock fallback."""
        if not self.api_key or self.provider == "mock":
            logger.info("Using mock LLM provider completion.")
            return self._mock_completion(prompt, system_prompt)

        # TODO: Extend with real OpenAI, Gemini, or Anthropic client calls when API key is provided
        logger.info(f"Generating via provider '{self.provider}' model '{self.model}'")
        return self._mock_completion(prompt, system_prompt)

    async def generate_structured(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate structured JSON completion."""
        raw_output = await self.generate(prompt, system_prompt)
        try:
            return json.loads(raw_output)
        except json.JSONDecodeError:
            return {"raw": raw_output}

    def _mock_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Fallback mock completion logic."""
        prompt_lower = prompt.lower()
        if "plan" in prompt_lower or "planner" in (system_prompt or "").lower():
            return json.dumps({
                "summary": "Implementation plan for request",
                "steps": [
                    {"step": 1, "description": "Inspect existing code"},
                    {"step": 2, "description": "Implement fix in target file"},
                    {"step": 3, "description": "Run tests and verify build"}
                ],
                "affected_files": ["app/main.py"],
                "acceptance_criteria": ["All tests pass cleanly"]
            }, indent=2)
        elif "review" in prompt_lower or "reviewer" in (system_prompt or "").lower():
            return json.dumps({
                "verdict": "APPROVE",
                "comments": "Changes look safe, adhere to patterns, and introduce no regressions."
            }, indent=2)
        else:
            return f"Mock response generated for prompt: '{prompt[:100]}...'"

llm_service = LLMService()
