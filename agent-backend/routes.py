from fastapi import APIRouter
from pydantic import BaseModel
from goal_agent import handle_goal_agent_prompt

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/goal-agent/prompt")
async def handle_prompt(request: PromptRequest):
    return await handle_goal_agent_prompt(request.prompt)