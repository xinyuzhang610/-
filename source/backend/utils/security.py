# utils/security.py
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
import jwt

def hash_password(password: str) -> str:
    """Hash a password with a per-password bcrypt salt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    """验证密码"""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except (ValueError, TypeError):
        return False

def generate_token(
    user_id: int,
    role: str,
    secret_key: str,
    *,
    jti: str | None = None,
    token_version: int = 0,
    expires_minutes: int = 60 * 12,
) -> str:
    """生成 JWT token"""
    payload = {
        "user_id": user_id,
        "role": role,
        "jti": jti,
        "token_version": token_version,
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

def verify_token(token: str, secret_key: str) -> Optional[dict]:
    """验证 JWT token"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
