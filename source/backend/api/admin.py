import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from api.dependencies import require_roles
from models.audit import AuditLog
from models.database import get_db
from models.recommend import RecommendRule
from models.tool import Tool
from models.user import User
from services.audit_service import write_audit
from services.session_service import revoke_user_sessions

router = APIRouter()

@router.get("/users")
def users(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    query = db.query(User).order_by(User.id.desc()); total = query.count(); rows = query.offset((page-1)*page_size).limit(page_size).all()
    return {"items": [{"id": u.id, "username": u.username, "name": u.name, "role": u.role, "is_active": u.is_active, "created_at": u.created_at} for u in rows], "total": total, "page": page, "page_size": page_size}

@router.patch("/users/{user_id}")
def update_user(user_id: int, payload: dict, db: Session = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="用户不存在")
    if "role" in payload and payload["role"] in {"teacher", "student", "admin"}: user.role = payload["role"]
    if "is_active" in payload:
        user.is_active = bool(payload["is_active"])
        if not user.is_active: revoke_user_sessions(db, user.id, "disabled")
    write_audit(db, "update_user", "user", user.id, actor_id=admin.id, details={"fields": list(payload) }); db.commit()
    return {"id": user.id, "role": user.role, "is_active": user.is_active}

@router.patch("/tools/{tool_id}/plaza")
def plaza_status(tool_id: int, payload: dict, db: Session = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool: raise HTTPException(status_code=404, detail="工具不存在")
    status = payload.get("plaza_status")
    if status not in {"published", "unlisted"}: raise HTTPException(status_code=422, detail="无效广场状态")
    tool.plaza_status = status; write_audit(db, "set_plaza_status", "tool", tool.id, actor_id=admin.id, details={"plaza_status": status}); db.commit(); return {"id": tool.id, "plaza_status": status}

@router.get("/recommend-rules")
def list_rules(db: Session = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    return db.query(RecommendRule).order_by(RecommendRule.priority.desc(), RecommendRule.id.desc()).all()

@router.post("/recommend-rules")
def create_rule(payload: dict, db: Session = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    rule = RecommendRule(subject=payload.get("subject"), category=payload.get("category"), need_type=payload.get("need_type"), tool_ids=payload.get("tool_ids", []), priority=payload.get("priority", 0), is_active=payload.get("is_active", True)); db.add(rule); db.flush(); write_audit(db, "create_recommend_rule", "recommend_rule", rule.id, actor_id=admin.id); db.commit(); return rule

@router.patch("/recommend-rules/{rule_id}")
def update_rule(rule_id: int, payload: dict, db: Session = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    rule = db.query(RecommendRule).filter(RecommendRule.id == rule_id).first()
    if not rule: raise HTTPException(status_code=404, detail="推荐规则不存在")
    for field in ("subject", "category", "need_type", "tool_ids", "priority", "is_active"):
        if field in payload: setattr(rule, field, payload[field])
    write_audit(db, "update_recommend_rule", "recommend_rule", rule.id, actor_id=admin.id, details={"fields": list(payload)}); db.commit(); return rule

@router.delete("/recommend-rules/{rule_id}", status_code=204)
def delete_rule(rule_id: int, db: Session = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    rule = db.query(RecommendRule).filter(RecommendRule.id == rule_id).first()
    if not rule: raise HTTPException(status_code=404, detail="推荐规则不存在")
    write_audit(db, "delete_recommend_rule", "recommend_rule", rule.id, actor_id=admin.id); db.delete(rule); db.commit()

@router.get("/audit-logs")
def audit_logs(page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100), db: Session = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    query = db.query(AuditLog).order_by(AuditLog.created_at.desc()); total = query.count(); rows = query.offset((page-1)*page_size).limit(page_size).all()
    return {"items": rows, "total": total, "page": page, "page_size": page_size}

@router.get("/audit-logs/export")
def export_audit_logs(db: Session = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    output = io.StringIO(); writer = csv.writer(output); writer.writerow(["id", "actor_id", "action", "resource_type", "resource_id", "result", "created_at"])
    for row in db.query(AuditLog).order_by(AuditLog.created_at.desc()).all(): writer.writerow([row.id, row.actor_id, row.action, row.resource_type, row.resource_id, row.result, row.created_at])
    return StreamingResponse(iter([output.getvalue().encode("utf-8-sig")]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=audit-logs.csv"})
