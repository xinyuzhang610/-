from sqlalchemy.orm import Session

from models.audit import AuditLog


def write_audit(
    db: Session,
    action: str,
    resource_type: str,
    resource_id: str | int | None = None,
    *,
    actor_id: int | None = None,
    result: str = "success",
    details: dict | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> AuditLog:
    record = AuditLog(
        actor_id=actor_id,
        action=action,
        resource_type=resource_type,
        resource_id=str(resource_id) if resource_id is not None else None,
        result=result,
        details=details,
        ip_address=ip_address,
        user_agent=(user_agent or "")[:500] or None,
    )
    db.add(record)
    return record
