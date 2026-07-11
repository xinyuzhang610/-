from sqlalchemy import Column, Integer, String, Text, Enum, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from .database import Base

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(Enum('文科', '理科', '通用'), nullable=False)
    subject = Column(String(50))
    icon = Column(String(50))
    prompt_template = Column(Text, nullable=False)
    interface_config = Column(JSON)
    creator_id = Column(Integer, ForeignKey("users.id"))
    is_preset = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    share_code = Column(String(20), unique=True)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class ToolTemplate(Base):
    __tablename__ = "tool_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(Enum('文科', '理科', '通用'), nullable=False)
    subject = Column(String(50))
    description = Column(Text)
    prompt_template = Column(Text, nullable=False)
    default_config = Column(JSON)
    icon = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())