from sqlalchemy.orm import Session
from models.recommend import RecommendRule
from models.tool import Tool
from services.tool_access_service import is_plaza_visible, public_tool_payload

def recommend_tools(db: Session, category: str | None, subject: str | None, need_type: str | None):
    rules = db.query(RecommendRule).filter(RecommendRule.is_active.is_(True), RecommendRule.need_type == need_type).all()
    matching = [r for r in rules if (not r.subject or r.subject == subject) and (not r.category or r.category == category)]
    matching.sort(key=lambda r: (2 if subject and r.subject == subject else 1 if category and r.category == category else 0, r.priority or 0), reverse=True)
    if matching:
        tools = db.query(Tool).filter(Tool.id.in_(matching[0].tool_ids or [])).all()
        return [public_tool_payload(t) for t in tools if is_plaza_visible(t)], matching[0]
    fallback = db.query(Tool).filter(Tool.is_preset.is_(True), Tool.deleted_at.is_(None))
    if category: fallback = fallback.filter(Tool.category == category)
    return [public_tool_payload(t) for t in fallback.order_by(Tool.usage_count.desc()).limit(6).all() if is_plaza_visible(t)], None
