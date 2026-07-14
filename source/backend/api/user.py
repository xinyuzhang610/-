from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from schemas.user import UserCreate, UserResponse, LoginRequest, TokenResponse, UserUpdate
from services.user_service import create_user, authenticate_user, get_user_by_id, get_user_by_username, update_user
from utils.security import generate_token
from config import settings
from api.dependencies import get_current_user
from models.user import User

router = APIRouter()

# 注册接口
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    if user.role.value == "admin":
        raise HTTPException(status_code=403, detail="管理员账号只能由受控初始化流程创建")
    # 检查用户名是否已存在
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 创建新用户
    db_user = create_user(db, user)
    return db_user

# 登录接口
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """用户登录"""
    # 验证用户
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 生成token
    access_token = generate_token(user.id, user.role, settings.SECRET_KEY)

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.from_orm(user)
    )

# 获取用户信息
@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """获取用户信息"""
    return current_user

# 更新用户信息
@router.put("/profile", response_model=UserResponse)
def update_profile(user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """更新用户信息"""
    update_data = user_update.model_dump(exclude_unset=True)
    user = update_user(db, current_user.id, update_data)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user
