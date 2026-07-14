# utils/security.py
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
import jwt

# 密码哈希 salt
SALT = "zjiaotong_salt_2024"

def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(f"{password}{SALT}".encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """验证密码"""
    return hash_password(password) == hashed_password

def generate_token(user_id: int, role: str, secret_key: str) -> str:
    """生成 JWT token"""
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(days=7)
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
