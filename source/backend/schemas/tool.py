from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ToolCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str  # '文科', '理科', '通用'
    subject: Optional[str] = None
    icon: Optional[str] = None
    prompt_template: str
    interface_config: Optional[dict] = None
    is_preset: bool = False
    is_public: bool = True

class ToolResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: str
    subject: Optional[str]
    icon: Optional[str]
    prompt_template: str
    interface_config: Optional[dict]
    creator_id: Optional[int]
    is_preset: bool
    is_public: bool
    share_code: Optional[str]
    usage_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ToolListResponse(BaseModel):
    total: int
    items: List[ToolResponse]
