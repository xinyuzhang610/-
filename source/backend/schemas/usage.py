from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UsageLogResponse(BaseModel):
    id: int
    tool_id: int
    user_id: Optional[int]
    input_text: Optional[str]
    output_text: Optional[str]
    session_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_tools: int
    total_users: int
    today_usage: int
    weekly_trend: List[dict]
    top_tools: List[dict]
    recent_logs: List[UsageLogResponse]
