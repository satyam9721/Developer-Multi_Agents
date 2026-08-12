from typing import Any, Dict
from app.config.settings import settings

class HealthCheckService:
    """Verifies system health, configuration, and environment services."""

    @staticmethod
    def get_system_health() -> Dict[str, Any]:
        return {
            "status": "healthy",
            "environment": settings.APP_ENV,
            "llm_provider": settings.LLM_PROVIDER,
            "workspace_root": settings.WORKSPACE_ROOT,
            "services": {
                "database": "configured" if settings.DATABASE_URL else "unconfigured",
                "redis": "configured" if settings.REDIS_URL else "unconfigured",
                "github": "configured" if settings.GITHUB_TOKEN else "unconfigured"
            }
        }

health_service = HealthCheckService()
