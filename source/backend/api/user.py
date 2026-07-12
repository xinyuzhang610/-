from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse, LoginRequest, TokenResponse, UserUpdate
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import settings
from typing import List

router = APIRouter()

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = "your-secret-key-keep-it-secret"  # 生产环境应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24小时

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 注册接口
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 创建新用户
    db_user = User(
        username=user.username,
        password_hash=get_password_hash(user.password),
        role=user.role,
        name=user.name,
        school=user.school,
        subject=user.subject,
        grade=user.grade
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 登录接口
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 查找用户
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 验证密码
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 生成token
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.from_orm(user)
    )

# 获取用户信息
@router.get("/profile/{user_id}", response_model=UserResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

# 更新用户信息
@router.put("/profile/{user_id}", response_model=UserResponse)
def update_profile(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user