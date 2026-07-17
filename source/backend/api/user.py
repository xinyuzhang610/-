from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from models.database import get_db
from schemas.user import PasswordChangeRequest, UserCreate, UserResponse, LoginRequest, TokenResponse, UserUpdate
from services.audit_service import write_audit
from services.captcha_service import CaptchaError, verify_captcha
from services.session_service import create_session, revoke_session, revoke_user_sessions
from services.user_service import (
    create_user,
    get_user_by_username,
    is_user_locked,
    register_failed_login,
    register_successful_login,
    update_user,
    validate_password_strength,
)
from utils.security import hash_password, verify_password
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
    try:
        db_user = create_user(db, user)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    write_audit(db, "register", "user", db_user.id, actor_id=db_user.id)
    db.commit()
    return db_user

# 登录接口
@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, http_request: Request, db: Session = Depends(get_db)):
    """用户登录"""
    try:
        await verify_captcha(request.captcha_token, http_request.client.host if http_request.client else None)
    except CaptchaError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    user = get_user_by_username(db, request.username)
    if not user:
        write_audit(db, "login", "user", result="failed", details={"username": request.username})
        db.commit()
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if request.expected_role and request.expected_role != user.role:
        role_label = "教师" if request.expected_role == "teacher" else "学生"
        raise HTTPException(status_code=403, detail=f"该账号不是{role_label}账号，请切换到{'教师' if user.role == 'teacher' else '学生'}登录入口")
    if not user.is_active:
        write_audit(db, "login", "user", user.id, actor_id=user.id, result="failed", details={"reason": "disabled"})
        db.commit()
        raise HTTPException(status_code=403, detail="账号已被禁用")
    if is_user_locked(user):
        raise HTTPException(status_code=423, detail="账号已锁定，请稍后再试")
    if not verify_password(request.password, user.password_hash):
        register_failed_login(user)
        write_audit(db, "login", "user", user.id, actor_id=user.id, result="failed", details={"reason": "invalid_password"})
        db.commit()
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    register_successful_login(user)
    session = create_session(
        db,
        user,
        http_request.client.host if http_request.client else None,
        http_request.headers.get("user-agent"),
    )
    write_audit(db, "login", "user", user.id, actor_id=user.id)
    db.commit()

    # 生成token
    access_token = generate_token(
        user.id,
        user.role,
        settings.SECRET_KEY,
        jti=session.jti,
        token_version=user.token_version,
        expires_minutes=settings.JWT_MAX_SESSION_HOURS * 60,
    )

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


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payload = request.state.jwt_payload if hasattr(request.state, "jwt_payload") else None
    # get_current_user already validates the JWT. Decode only the jti needed for revocation.
    from utils.security import verify_token

    authorization = request.headers.get("authorization", "")
    token = authorization.removeprefix("Bearer ").strip()
    payload = verify_token(token, settings.SECRET_KEY) if token else payload
    if payload and payload.get("jti"):
        revoke_session(db, payload["jti"])
        write_audit(db, "logout", "user", current_user.id, actor_id=current_user.id)
        db.commit()


@router.post("/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    request: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not verify_password(request.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="旧密码不正确")
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=400, detail="两次输入的新密码不一致")
    try:
        validate_password_strength(request.new_password)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    current_user.password_hash = hash_password(request.new_password)
    current_user.password_changed_at = datetime.utcnow()
    current_user.token_version += 1
    revoke_user_sessions(db, current_user.id, "password_changed")
    write_audit(db, "change_password", "user", current_user.id, actor_id=current_user.id)
    db.commit()
