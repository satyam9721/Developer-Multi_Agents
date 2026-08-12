from app.policies.permissions import PolicyViolationError

class ProductionPolicy:
    """Enforces production deployment & merge policy guardrails."""

    @staticmethod
    def validate_production_deployment(environment: str, user_approved: bool) -> bool:
        """Ensure deployment to production requires explicit approval."""
        if environment.lower() in ["prod", "production"] and not user_approved:
            raise PolicyViolationError("Production deployment requires explicit user authorization.")
        return True
