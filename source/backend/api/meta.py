"""Unified metadata API — single source of truth for subjects, need types, and approaches."""

from fastapi import APIRouter

router = APIRouter()

SUBJECTS = [
    {"code": "chinese", "name": "语文", "category": "文科", "order": 1},
    {"code": "english", "name": "英语", "category": "文科", "order": 2},
    {"code": "history", "name": "历史", "category": "文科", "order": 3},
    {"code": "geography", "name": "地理", "category": "文科", "order": 4},
    {"code": "politics", "name": "政治", "category": "文科", "order": 5},
    {"code": "math", "name": "数学", "category": "理科", "order": 6},
    {"code": "physics", "name": "物理", "category": "理科", "order": 7},
    {"code": "chemistry", "name": "化学", "category": "理科", "order": 8},
    {"code": "biology", "name": "生物", "category": "理科", "order": 9},
    {"code": "it", "name": "信息技术", "category": "理科", "order": 10},
    {"code": "general", "name": "通用", "category": "通用", "order": 11},
]

NEED_TYPES = [
    {"code": "pre_class", "name": "课前备课", "description": "组织资料与课堂结构"},
    {"code": "in_class", "name": "课堂教学", "description": "提问、演示与实时参与"},
    {"code": "after_class", "name": "课后辅导", "description": "答疑与个性化支持"},
    {"code": "interest", "name": "兴趣激发", "description": "让知识变得可探索"},
]

LEARNING_DIFFICULTIES = [
    {"code": "cant_read", "name": "读不懂题"},
    {"code": "no_approach", "name": "找不到思路"},
    {"code": "cant_focus", "name": "难以专注"},
]

LEARNING_APPROACHES = [
    {"code": "concept", "name": "概念辨析"},
    {"code": "step_by_step", "name": "分步推导"},
    {"code": "case_study", "name": "案例启发"},
    {"code": "practice", "name": "练习巩固"},
]


@router.get("/subjects")
def get_subjects(category: str | None = None):
    items = SUBJECTS
    if category:
        items = [s for s in items if s["category"] == category]
    return items


@router.get("/need-types")
def get_need_types():
    return NEED_TYPES


@router.get("/learning-difficulties")
def get_learning_difficulties():
    return LEARNING_DIFFICULTIES


@router.get("/learning-approaches")
def get_learning_approaches():
    return LEARNING_APPROACHES
