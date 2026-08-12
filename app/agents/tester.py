import os
from typing import Any, Dict
from app.agents.base import AgentContext, BaseAgent
from app.tools.shell import shell_tool

class TesterAgent(BaseAgent):
    name = "tester"
    description = "Detects test framework, runs unit & integration tests, linting, and build checks."
    system_prompt = "You are the TesterAgent. Execute build and test commands and analyze failure logs."

    async def run(self, context: AgentContext) -> Dict[str, Any]:
        workspace_dir = context.workspace_path

        # Auto-detect test framework
        test_command = "pytest"
        if os.path.exists(os.path.join(workspace_dir, "package.json")):
            test_command = "npm test"

        # Execute test command safely via shell tool
        exec_result = shell_tool.execute_with_policy(
            agent_role=self.name,
            command=test_command,
            workspace_dir=workspace_dir,
            timeout=30
        )

        passed = exec_result.get("exit_code") == 0

        return {
            "summary": f"Executed tests with command '{test_command}'",
            "passed": passed,
            "exit_code": exec_result.get("exit_code"),
            "stdout": exec_result.get("stdout", ""),
            "stderr": exec_result.get("stderr", ""),
            "failures": [] if passed else ["Tests failed or test framework returned non-zero exit code."]
        }

tester_agent = TesterAgent()
