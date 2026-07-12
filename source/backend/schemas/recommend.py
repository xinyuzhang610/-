from pydantic import BaseModel
from typing import List, Optional

class RecommendRequest(BaseModel):
    step: int
    category: Optional[str] = None
    need_type: Optional[str] = None

class RecommendResponse(BaseModel):
    step: int
    message: str
    options: Optional[List[dict]] = None
    tools: Optional[List[dict]] = None
