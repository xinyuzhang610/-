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
    is_public: bool = True


class ToolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subject: Optional[str] = None
    icon: Optional[str] = None
    prompt_template: Optional[str] = None
    interface_config: Optional[dict] = None
    external_platform_url: Optional[str] = None
    plaza_status: Optional[str] = None


class ShareSettings(BaseModel):
    enabled: bool = True
    expires_at: Optional[datetime] = None


class ToolPublicResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: str
    subject: Optional[str]
    icon: Optional[str]
    share_code: Optional[str]
    usage_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

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
    template_source_id: Optional[int] = None
    source_type: str = "manual"
    deleted_at: Optional[datetime] = None
    plaza_status: str = "published"
    share_enabled: bool = True
    share_expires_at: Optional[datetime] = None
    external_platform_url: Optional[str] = None
    usage_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ToolListResponse(BaseModel):
    total: int
    items: List[ToolResponse]
    page: int = 1
    page_size: int = 20


class PublicToolListResponse(BaseModel):
    total: int
    items: List[ToolPublicResponse]
    page: int = 1
    page_size: int = 20
