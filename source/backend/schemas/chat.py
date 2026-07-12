from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    tool_id: Optional[int] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    tool_name: Optional[str] = None
