from sqlalchemy.orm import Session
from models.recommend import RecommendRule
from models.tool import Tool
from services.tool_access_service import is_plaza_visible, public_tool_payload

# Per-subject, per-need_type tool recommendations (tool names, ordered by relevance)
# Ensures 语文 never returns 公式推导助手, etc.
SUBJECT_TOOL_MAP = {
    "语文": {
        "课前备课": ["古诗词趣味赏析", "阅读理解辅助", "作文灵感助手"],
        "课堂教学": ["诗词飞花令", "古诗词趣味赏析", "阅读理解辅助"],
        "课后辅导": ["作文灵感助手", "阅读理解辅助", "古诗词趣味赏析"],
        "兴趣激发": ["诗词飞花令", "古诗词趣味赏析", "名词解释器"],
    },
    "英语": {
        "课前备课": ["英语单词卡片", "AI学习助手", "知识卡片生成器"],
        "课堂教学": ["英语单词卡片", "AI学习助手", "诗词飞花令"],
        "课后辅导": ["英语单词卡片", "AI学习助手", "阅读理解辅助"],
        "兴趣激发": ["英语单词卡片", "诗词飞花令", "知识卡片生成器"],
    },
    "历史": {
        "课前备课": ["名词解释器", "知识卡片生成器", "思维导图助手"],
        "课堂教学": ["名词解释器", "思维导图助手", "AI学习助手"],
        "课后辅导": ["知识卡片生成器", "AI学习助手", "思维导图助手"],
        "兴趣激发": ["古诗词趣味赏析", "思维导图助手", "知识卡片生成器"],
    },
    "地理": {
        "课前备课": ["知识卡片生成器", "思维导图助手", "AI学习助手"],
        "课堂教学": ["思维导图助手", "数据分析助手", "知识卡片生成器"],
        "课后辅导": ["知识卡片生成器", "AI学习助手", "概念辨析器"],
        "兴趣激发": ["思维导图助手", "知识卡片生成器", "逻辑思维训练"],
    },
    "政治": {
        "课前备课": ["名词解释器", "阅读理解辅助", "知识卡片生成器"],
        "课堂教学": ["名词解释器", "逻辑思维训练", "AI学习助手"],
        "课后辅导": ["知识卡片生成器", "AI学习助手", "阅读理解辅助"],
        "兴趣激发": ["逻辑思维训练", "名词解释器", "思维导图助手"],
    },
    "数学": {
        "课前备课": ["公式推导助手", "错题分析器", "数据分析助手"],
        "课堂教学": ["逻辑思维训练", "公式推导助手", "数据分析助手"],
        "课后辅导": ["错题分析器", "公式推导助手", "逻辑思维训练"],
        "兴趣激发": ["逻辑思维训练", "数据分析助手", "知识卡片生成器"],
    },
    "物理": {
        "课前备课": ["实验模拟讲解", "概念辨析器", "公式推导助手"],
        "课堂教学": ["实验模拟讲解", "概念辨析器", "数据分析助手"],
        "课后辅导": ["概念辨析器", "错题分析器", "实验模拟讲解"],
        "兴趣激发": ["实验模拟讲解", "逻辑思维训练", "知识卡片生成器"],
    },
    "化学": {
        "课前备课": ["实验模拟讲解", "概念辨析器", "知识卡片生成器"],
        "课堂教学": ["实验模拟讲解", "逻辑思维训练", "知识卡片生成器"],
        "课后辅导": ["概念辨析器", "错题分析器", "知识卡片生成器"],
        "兴趣激发": ["实验模拟讲解", "逻辑思维训练", "数据分析助手"],
    },
    "生物": {
        "课前备课": ["概念辨析器", "知识卡片生成器", "思维导图助手"],
        "课堂教学": ["实验模拟讲解", "逻辑思维训练", "知识卡片生成器"],
        "课后辅导": ["概念辨析器", "知识卡片生成器", "AI学习助手"],
        "兴趣激发": ["实验模拟讲解", "思维导图助手", "知识卡片生成器"],
    },
    "信息技术": {
        "课前备课": ["数据分析助手", "逻辑思维训练", "知识卡片生成器"],
        "课堂教学": ["数据分析助手", "逻辑思维训练", "AI学习助手"],
        "课后辅导": ["数据分析助手", "AI学习助手", "知识卡片生成器"],
        "兴趣激发": ["逻辑思维训练", "数据分析助手", "思维导图助手"],
    },
}

# Category-level fallback for unspecified subjects
CATEGORY_NEED_MAP = {
    ("文科", "课前备课"): ["古诗词趣味赏析", "阅读理解辅助", "知识卡片生成器"],
    ("文科", "课堂教学"): ["诗词飞花令", "名词解释器", "AI学习助手"],
    ("文科", "课后辅导"): ["作文灵感助手", "阅读理解辅助", "知识卡片生成器"],
    ("文科", "兴趣激发"): ["诗词飞花令", "古诗词趣味赏析", "思维导图助手"],
    ("理科", "课前备课"): ["公式推导助手", "实验模拟讲解", "知识卡片生成器"],
    ("理科", "课堂教学"): ["逻辑思维训练", "实验模拟讲解", "数据分析助手"],
    ("理科", "课后辅导"): ["错题分析器", "公式推导助手", "概念辨析器"],
    ("理科", "兴趣激发"): ["逻辑思维训练", "数据分析助手", "思维导图助手"],
}

ALL_NEED_TYPES = {"课前备课", "课堂教学", "课后辅导", "兴趣激发"}


def _resolve_tool_names(subject: str | None, need_type: str | None) -> list[str]:
    """Resolve ordered tool name list for a given subject + need_type."""
    if not need_type:
        return []
    if subject and subject in SUBJECT_TOOL_MAP:
        return SUBJECT_TOOL_MAP[subject].get(need_type, [])
    return []


def _query_tools_by_names(db: Session, names: list[str]) -> list[Tool]:
    """Query preset tools matching the given names, preserving name order."""
    if not names:
        return []
    results = db.query(Tool).filter(
        Tool.is_preset.is_(True),
        Tool.deleted_at.is_(None),
        Tool.name.in_(names),
    ).all()
    ordered = sorted(results, key=lambda t: names.index(t.name) if t.name in names else 99)
    return ordered


def recommend_tools(db: Session, category: str | None, subject: str | None, need_type: str | None):
    # 1) Exact DB rule match (covers custom / overridden rules)
    if need_type:
        rules = db.query(RecommendRule).filter(
            RecommendRule.is_active.is_(True),
            RecommendRule.need_type == need_type,
        ).all()
        matching = [
            r for r in rules
            if (not r.subject or r.subject == subject)
            and (not r.category or r.category == category)
        ]
        matching.sort(
            key=lambda r: (
                2 if subject and r.subject == subject else 1 if category and r.category == category else 0,
                r.priority or 0,
            ),
            reverse=True,
        )
        if matching:
            tools = db.query(Tool).filter(Tool.id.in_(matching[0].tool_ids or [])).all()
            ordered = sorted(
                tools,
                key=lambda t: matching[0].tool_ids.index(str(t.id))
                if str(t.id) in (matching[0].tool_ids or [])
                else 99,
            )
            return [public_tool_payload(t) for t in ordered if is_plaza_visible(t)], matching[0]

    # 2) Subject-specific fallback — ensures 语文 never returns 理科 tools
    if subject and need_type:
        names = _resolve_tool_names(subject, need_type)
        if names:
            tools = _query_tools_by_names(db, names)
            if tools:
                return [public_tool_payload(t) for t in tools if is_plaza_visible(t)], None

    # 3) Category-level fallback (subject not specified or no match)
    if category and need_type:
        cat_names = CATEGORY_NEED_MAP.get((category, need_type), [])
        if cat_names:
            tools = _query_tools_by_names(db, cat_names)
            if tools:
                return [public_tool_payload(t) for t in tools if is_plaza_visible(t)], None

    # 4) Ultimate fallback: popular presets in same category
    fallback = db.query(Tool).filter(Tool.is_preset.is_(True), Tool.deleted_at.is_(None))
    if category:
        fallback = fallback.filter(Tool.category == category)
    return [
        public_tool_payload(t)
        for t in fallback.order_by(Tool.usage_count.desc()).limit(6).all()
        if is_plaza_visible(t)
    ], None


SUBJECT_CATEGORY = {
    "语文": "文科", "英语": "文科", "历史": "文科", "政治": "文科", "地理": "文科",
    "数学": "理科", "物理": "理科", "化学": "理科", "生物": "理科", "信息技术": "理科",
    "通用": "通用",
}

# Student guidance uses deterministic matching as well. It is intentionally
# separate from the teacher map because its input is difficulty + approach.
STUDENT_TOOL_MAP = {
    ("读不懂题", "概念辨析"): ["概念辨析器", "名词解释器", "阅读理解辅助"],
    ("读不懂题", "分步推导"): ["公式推导助手", "阅读理解辅助", "实验模拟讲解"],
    ("读不懂题", "案例启发"): ["古诗词趣味赏析", "实验模拟讲解", "知识卡片生成器"],
    ("读不懂题", "练习巩固"): ["错题分析器", "英语单词卡片", "逻辑思维训练"],
    ("找不到思路", "概念辨析"): ["概念辨析器", "名词解释器", "AI学习助手"],
    ("找不到思路", "分步推导"): ["公式推导助手", "错题分析器", "思维导图助手"],
    ("找不到思路", "案例启发"): ["作文灵感助手", "古诗词趣味赏析", "实验模拟讲解"],
    ("找不到思路", "练习巩固"): ["逻辑思维训练", "错题分析器", "知识卡片生成器"],
    ("难以专注", "概念辨析"): ["知识卡片生成器", "名词解释器", "AI学习助手"],
    ("难以专注", "分步推导"): ["知识卡片生成器", "逻辑思维训练", "思维导图助手"],
    ("难以专注", "案例启发"): ["诗词飞花令", "逻辑思维训练", "实验模拟讲解"],
    ("难以专注", "练习巩固"): ["英语单词卡片", "逻辑思维训练", "知识卡片生成器"],
}

DIFFICULTY_ALIASES = {"cant_read": "读不懂题", "no_approach": "找不到思路", "cant_focus": "难以专注"}
APPROACH_ALIASES = {"concept": "概念辨析", "step_by_step": "分步推导", "case_study": "案例启发", "practice": "练习巩固"}


def recommend_student_tools(
    db: Session,
    difficulty: str | None,
    subject: str | None,
    approach: str | None,
):
    """Return a deterministic recommendation for the student's three-step flow."""
    difficulty = DIFFICULTY_ALIASES.get(difficulty, difficulty)
    approach = APPROACH_ALIASES.get(approach, approach)
    category = SUBJECT_CATEGORY.get(subject, "通用")
    names = STUDENT_TOOL_MAP.get((difficulty, approach), [])

    query = db.query(Tool).filter(
        Tool.is_preset.is_(True),
        Tool.deleted_at.is_(None),
        Tool.name.in_(names),
    )
    candidates = query.all()

    def score(tool):
        subject_score = 2 if subject and tool.subject == subject else 0
        category_score = 1 if tool.category == category else 0
        general_score = 1 if tool.category == "通用" else 0
        order = names.index(tool.name) if tool.name in names else 99
        return (-subject_score, -category_score, -general_score, order)

    ordered = sorted([tool for tool in candidates if is_plaza_visible(tool)], key=score)
    if not ordered:
        fallback_names = CATEGORY_NEED_MAP.get((category, "课后辅导"), [])
        fallback = db.query(Tool).filter(
            Tool.is_preset.is_(True),
            Tool.deleted_at.is_(None),
            Tool.name.in_(fallback_names),
        ).all()
        ordered = sorted(
            [tool for tool in fallback if is_plaza_visible(tool)],
            key=lambda tool: fallback_names.index(tool.name) if tool.name in fallback_names else 99,
        )

    reason = f"根据“{difficulty or '当前学习阻力'} · {subject or '通用学科'} · {approach or '学习方式'}”进行规则匹配"
    return [public_tool_payload(tool) for tool in ordered[:6]], reason
