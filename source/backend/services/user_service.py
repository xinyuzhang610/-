# services/user_service.py
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, LoginRequest
from utils.security import hash_password, verify_password

def create_user(db: Session, user_data: UserCreate):
    """创建新用户"""
    hashed_password = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        password_hash=hashed_password,
        role=user_data.role.value,
        name=user_data.name,
        school=user_data.school,
        subject=user_data.subject,
        grade=user_data.grade
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """验证用户登录"""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def get_user_by_id(db: Session, user_id: int):
    """根据ID获取用户"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """根据用户名获取用户"""
    return db.query(User).filter(User.username == username).first()

def update_user(db: Session, user_id: int, user_data: dict):
    """更新用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in user_data.items():
        if value is not None:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
