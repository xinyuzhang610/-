from pydantic import BaseModel
from typing import Optional, Literal

class ChatRequest(BaseModel):
    message: str
    tool_id: Optional[int] = None
    session_id: Optional[str] = None
    # Required for anonymous access through a teacher-generated share link.
    # It prevents guessing a numeric tool id from becoming public AI access.
    share_code: Optional[str] = None
    usage_mode: Literal["student_use", "teacher_preview"] = "student_use"

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    tool_name: Optional[str] = None
