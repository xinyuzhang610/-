from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from config import settings
from models.session import AuthSession
from models.user import User


def create_session(db: Session, user: User, ip_address: str | None = None, user_agent: str | None = None) -> AuthSession:
    now = datetime.utcnow()
    session = AuthSession(
        jti=uuid4().hex,
        user_id=user.id,
        issued_at=now,
        last_seen_at=now,
        expires_at=now + timedelta(hours=settings.JWT_MAX_SESSION_HOURS),
        ip_address=ip_address,
        user_agent=(user_agent or "")[:500] or None,
    )
    db.add(session)
    db.flush()
    return session


def validate_session(db: Session, user: User, jti: str | None, now: datetime | None = None) -> AuthSession | None:
    if not jti or not user.is_active:
        return None
    current_time = now or datetime.utcnow()
    session = db.query(AuthSession).filter(AuthSession.jti == jti, AuthSession.user_id == user.id).first()
    if not session or session.revoked_at or session.expires_at <= current_time:
        return None
    if session.last_seen_at + timedelta(minutes=settings.JWT_IDLE_MINUTES) <= current_time:
        session.revoked_at = current_time
        session.revoke_reason = "idle_timeout"
        db.commit()
        return None
    if (current_time - session.last_seen_at).total_seconds() >= settings.SESSION_TOUCH_INTERVAL_SECONDS:
        session.last_seen_at = current_time
        db.commit()
    return session


def revoke_user_sessions(db: Session, user_id: int, reason: str, except_jti: str | None = None) -> int:
    query = db.query(AuthSession).filter(AuthSession.user_id == user_id, AuthSession.revoked_at.is_(None))
    if except_jti:
        query = query.filter(AuthSession.jti != except_jti)
    sessions = query.all()
    now = datetime.utcnow()
    for session in sessions:
        session.revoked_at = now
        session.revoke_reason = reason
    return len(sessions)


def revoke_session(db: Session, jti: str, reason: str = "logout") -> bool:
    session = db.query(AuthSession).filter(AuthSession.jti == jti, AuthSession.revoked_at.is_(None)).first()
    if not session:
        return False
    session.revoked_at = datetime.utcnow()
    session.revoke_reason = reason
    return True
