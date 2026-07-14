from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum('teacher', 'student', 'admin'), nullable=False)
    name = Column(String(50))
    school = Column(String(100))
    subject = Column(String(50))
    grade = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())