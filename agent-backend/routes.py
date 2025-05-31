from fastapi import APIRouter
from pydantic import BaseModel
from goal_agent import handle_goal_agent_prompt
from summary_agent import generate_monthly_summary
from typing import Optional

router = APIRouter()

class GoalAgentRequest(BaseModel):
    prompt: str

@router.post("/goal-agent/prompt")
async def handle_prompt(request: GoalAgentRequest):
    return await handle_goal_agent_prompt(request.prompt)

class SummaryRequest(BaseModel):
    month: Optional[str] = None       # yyyy-mm; default = last complete month

@router.post("/monthly-summary")
async def monthly_summary(request: SummaryRequest):
    return await generate_monthly_summary(request.month)