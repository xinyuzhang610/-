from sqlalchemy.orm import Session
from models.recommend import RecommendRule
from models.tool import Tool
from services.tool_access_service import is_plaza_visible, public_tool_payload

# Fallback recommendations: each (category, need_type) pair gets its own set of tools
# When no explicit rule matches, this provides differentiated results per need type.
FALLBACK_NEED_TOOL_MAP = {
    ("文科", "课前备课"): ["古诗词趣味赏析", "阅读理解辅助", "名词解释器"],
    ("文科", "课堂教学"): ["诗词飞花令", "作文灵感助手", "英语单词卡片"],
    ("文科", "课后辅导"): ["作文灵感助手", "阅读理解辅助", "英语单词卡片"],
    ("文科", "兴趣激发"): ["诗词飞花令", "古诗词趣味赏析", "知识卡片生成器"],
    ("理科", "课前备课"): ["公式推导助手", "实验模拟讲解", "概念辨析器"],
    ("理科", "课堂教学"): ["逻辑思维训练", "实验模拟讲解", "数据分析助手"],
    ("理科", "课后辅导"): ["错题分析器", "公式推导助手", "概念辨析器"],
    ("理科", "兴趣激发"): ["逻辑思维训练", "数据分析助手", "知识卡片生成器"],
    ("通用", "课前备课"): ["知识卡片生成器", "思维导图助手", "AI学习助手"],
    ("通用", "课堂教学"): ["AI学习助手", "思维导图助手", "知识卡片生成器"],
    ("通用", "课后辅导"): ["AI学习助手", "知识卡片生成器", "错题分析器"],
    ("通用", "兴趣激发"): ["思维导图助手", "AI学习助手", "知识卡片生成器"],
}


def recommend_tools(db: Session, category: str | None, subject: str | None, need_type: str | None):
    rules = db.query(RecommendRule).filter(RecommendRule.is_active.is_(True), RecommendRule.need_type == need_type).all()
    matching = [r for r in rules if (not r.subject or r.subject == subject) and (not r.category or r.category == category)]
    matching.sort(key=lambda r: (2 if subject and r.subject == subject else 1 if category and r.category == category else 0, r.priority or 0), reverse=True)
    if matching:
        tools = db.query(Tool).filter(Tool.id.in_(matching[0].tool_ids or [])).all()
        return [public_tool_payload(t) for t in tools if is_plaza_visible(t)], matching[0]

    # Differentiated fallback: select tools by category + need_type
    fallback_names = FALLBACK_NEED_TOOL_MAP.get((category, need_type), [])
    if fallback_names:
        fallback = db.query(Tool).filter(
            Tool.is_preset.is_(True),
            Tool.deleted_at.is_(None),
            Tool.name.in_(fallback_names),
        )
        if category:
            fallback = fallback.filter(Tool.category == category)
        results = fallback.all()
        # Preserve the order defined in FALLBACK_NEED_TOOL_MAP
        ordered = sorted(results, key=lambda t: fallback_names.index(t.name) if t.name in fallback_names else 99)
        return [public_tool_payload(t) for t in ordered if is_plaza_visible(t)], None

    # Ultimate fallback: popular presets in the same category
    fallback = db.query(Tool).filter(Tool.is_preset.is_(True), Tool.deleted_at.is_(None))
    if category:
        fallback = fallback.filter(Tool.category == category)
    return [public_tool_payload(t) for t in fallback.order_by(Tool.usage_count.desc()).limit(6).all() if is_plaza_visible(t)], None
