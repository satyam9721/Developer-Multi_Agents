from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class AuthRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
async def login(req: AuthRequest):
    """Token authentication route stub."""
    return {"access_token": "mock-jwt-token-12345", "token_type": "bearer"}
