from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False)
    input_text = Column(Text)
    output_text = Column(Text)
    session_id = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())