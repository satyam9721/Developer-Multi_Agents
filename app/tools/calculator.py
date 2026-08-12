import ast
import operator
from typing import Any, Dict
from app.config.constants import PermissionType, RiskLevel
from app.tools.base import BaseTool

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Safely evaluate mathematical expressions."
    permission_type = PermissionType.READ
    risk_level = RiskLevel.READ_ONLY

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def _eval_node(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op = self.OPERATORS.get(type(node.op))
            if not op:
                raise ValueError(f"Unsupported operator: {type(node.op)}")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op = self.OPERATORS.get(type(node.op))
            if not op:
                raise ValueError(f"Unsupported operator: {type(node.op)}")
            return op(operand)
        raise ValueError("Invalid mathematical expression.")

    def run(self, expression: str) -> Dict[str, Any]:
        """Safely parse and evaluate math expression without eval."""
        try:
            parsed = ast.parse(expression, mode="eval")
            result = self._eval_node(parsed.body)
            return {"status": "success", "expression": expression, "result": result}
        except Exception as exc:
            return {"status": "error", "error": f"Failed to evaluate expression: {exc}"}

calculator_tool = CalculatorTool()
