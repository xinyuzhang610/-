from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from models.database import get_db
from models.tool import Tool
from models.usage import UsageLog
from services.tool_access_service import public_tool_payload

router = APIRouter()
CATEGORIES = [{"value": "文科", "label": "文科专区", "icon": "📚"}, {"value": "理科", "label": "理科专区", "icon": "🔬"}, {"value": "通用", "label": "通用工具", "icon": "🧭"}]

def visible(db):
    return db.query(Tool).filter(Tool.deleted_at.is_(None), Tool.plaza_status == "published")

@router.get("/")
def get_plaza(category: str | None = None, search: str | None = None, sort: str = Query("hot", pattern="^(hot|latest)$"), page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    query = visible(db)
    if category: query = query.filter(Tool.category == category)
    if search: query = query.filter(or_(Tool.name.contains(search), Tool.description.contains(search)))
    query = query.order_by(Tool.created_at.desc() if sort == "latest" else Tool.usage_count.desc())
    total = query.count(); items = [public_tool_payload(tool) for tool in query.offset((page - 1) * page_size).limit(page_size).all()]
    hot_tools = [public_tool_payload(tool) for tool in visible(db).order_by(Tool.usage_count.desc()).limit(5).all()]
    return {"categories": CATEGORIES, "items": items, "tools": items, "hot_tools": hot_tools, "total": total, "page": page, "page_size": page_size}

@router.get("/categories")
def get_categories(): return CATEGORIES

@router.get("/hot")
def get_hot_tools(limit: int = Query(5, ge=1, le=20), db: Session = Depends(get_db)):
    return [public_tool_payload(tool) for tool in visible(db).order_by(Tool.usage_count.desc()).limit(limit).all()]

@router.get("/weekly-ranking")
def weekly_ranking(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=7)
    rows = db.query(Tool, func.count(UsageLog.id).label("weekly_uses")).join(UsageLog, UsageLog.tool_id == Tool.id).filter(Tool.deleted_at.is_(None), Tool.plaza_status == "published", UsageLog.status == "completed", UsageLog.created_at >= since).group_by(Tool.id).order_by(func.count(UsageLog.id).desc()).limit(limit).all()
    return [{**public_tool_payload(tool), "weekly_uses": count} for tool, count in rows]
