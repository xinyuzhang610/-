from pydantic import BaseModel
from typing import List, Optional

class RecommendRequest(BaseModel):
    step: int
    category: Optional[str] = None
    subject: Optional[str] = None
    need_type: Optional[str] = None
    # Student guidance uses a different three-part input from the teacher
    # guidance flow.  Keep both contracts in one endpoint so the frontend
    # cannot accidentally send learning choices as a teacher need type.
    difficulty: Optional[str] = None
    approach: Optional[str] = None

class RecommendResponse(BaseModel):
    step: int
    message: str
    options: Optional[List[dict]] = None
    tools: Optional[List[dict]] = None
    reason: Optional[str] = None
