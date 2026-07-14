from pydantic import BaseModel
from typing import List, Optional

class PlazaTool(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: str
    subject: Optional[str]
    icon: Optional[str]
    usage_count: int
    share_code: Optional[str]

    class Config:
        from_attributes = True

class PlazaResponse(BaseModel):
    categories: List[dict]
    tools: List[PlazaTool]
    hot_tools: List[PlazaTool]
