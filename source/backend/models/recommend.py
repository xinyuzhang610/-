from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class RecommendRule(Base):
    __tablename__ = "recommend_rules"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(50))
    need_type = Column(String(50))
    tool_ids = Column(JSON)
    priority = Column(Integer, default=0)