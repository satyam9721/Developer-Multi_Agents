from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import llm_service

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str
    task_id: str = "default-task"

@router.post("")
async def chat(req: ChatRequest):
    """Chat assistant endpoint."""
    response = await llm_service.generate(req.message)
    return {"message": response, "task_id": req.task_id}
