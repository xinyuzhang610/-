from sqlalchemy import Boolean, Column, DateTime, Integer, String, JSON
from sqlalchemy.sql import func
from .database import Base

class RecommendRule(Base):
    __tablename__ = "recommend_rules"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(50))
    category = Column(String(20), nullable=True)
    need_type = Column(String(50))
    tool_ids = Column(JSON)
    priority = Column(Integer, default=0)
    is_active = Column(Boolean, nullable=False, default=True, server_default="1")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
