# services/user_service.py
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, LoginRequest
from utils.security import hash_password, verify_password


MAX_FAILED_LOGIN_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


def validate_password_strength(password: str) -> None:
    if len(password or "") < 8:
        raise ValueError("密码至少需要 8 位")
    if not any(character.isalpha() for character in password):
        raise ValueError("密码必须包含字母")
    if not any(character.isdigit() for character in password):
        raise ValueError("密码必须包含数字")


def is_user_locked(user: User, now: datetime | None = None) -> bool:
    return bool(user.locked_until and user.locked_until > (now or datetime.utcnow()))


def register_failed_login(user: User, now: datetime | None = None) -> None:
    current_time = now or datetime.utcnow()
    user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
    if user.failed_login_attempts >= MAX_FAILED_LOGIN_ATTEMPTS:
        user.locked_until = current_time + timedelta(minutes=LOCKOUT_MINUTES)


def register_successful_login(user: User, now: datetime | None = None) -> None:
    current_time = now or datetime.utcnow()
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login_at = current_time

def create_user(db: Session, user_data: UserCreate):
    """创建新用户"""
    validate_password_strength(user_data.password)
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
