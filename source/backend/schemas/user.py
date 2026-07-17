from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    teacher = "teacher"
    student = "student"
    admin = "admin"

# 用户基础模型
class UserBase(BaseModel):
    username: str
    role: UserRole
    name: Optional[str] = None
    school: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None

# 用户创建模型
class UserCreate(UserBase):
    password: str

# 用户更新模型
class UserUpdate(BaseModel):
    name: Optional[str] = None
    school: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None

# 用户响应模型
class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool = True
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# 登录请求模型
class LoginRequest(BaseModel):
    username: str
    password: str
    captcha_token: Optional[str] = None
    expected_role: Optional[str] = None


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

# 登录响应模型
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
