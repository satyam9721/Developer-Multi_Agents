from fastapi import APIRouter
from app.deployments.healthcheck import health_service

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    """System health check endpoint."""
    return health_service.get_system_health()
