"""Seed deterministic local demo data after Alembic migrations.

This script is intentionally local-only and idempotent. It never drops tables,
deletes rows, or contains a database password. Configure DATABASE_URL in .env
before running it.
"""

from datetime import datetime, timezone

from sqlalchemy import select

from init_db import insert_preset_templates, insert_preset_tools
from models.database import SessionLocal
from models.recommend import RecommendRule
from models.tool import Tool, ToolTemplate
from models.user import User
from services.recommend_service import SUBJECT_CATEGORY, SUBJECT_TOOL_MAP
from utils.security import hash_password


DEMO_USERS = (
    {
        "username": "teacher_demo",
        "password": "Teacher2026",
        "role": "teacher",
        "name": "演示教师",
        "school": "智教通演示学校",
        "subject": "语文",
        "grade": "高中",
    },
    {
        "username": "student_demo",
        "password": "Student2026",
        "role": "student",
        "name": "演示学生",
        "school": "智教通演示学校",
        "subject": "语文",
        "grade": "高中",
    },
    {
        "username": "admin_demo",
        "password": "Admin2026",
        "role": "admin",
        "name": "演示管理员",
        "school": "智教通演示学校",
    },
)

LEGACY_TEST_USER_PREFIXES = ("e2e_", "verify_", "ai_")
LEGACY_TEST_TOOL_MARKERS = ("E2E Tool ", "verify-tool-", "数据分析助手（副本）")


def hide_legacy_test_rows(session) -> tuple[int, int]:
    """Hide test-run accounts/tools left by old integration scripts."""
    legacy_users = session.scalars(select(User)).all()
    legacy_user_ids = {
        user.id
        for user in legacy_users
        if user.username.startswith(LEGACY_TEST_USER_PREFIXES)
    }
    disabled_users = 0
    for user in legacy_users:
        if user.id in legacy_user_ids and user.is_active:
            user.is_active = False
            disabled_users += 1

    hidden_tools = 0
    for tool in session.scalars(select(Tool)).all():
        is_legacy_tool = (
            not tool.is_preset
            and (tool.creator_id in legacy_user_ids or any(marker in (tool.name or "") for marker in LEGACY_TEST_TOOL_MARKERS))
        )
        if is_legacy_tool and (tool.deleted_at is None or tool.plaza_status != "unlisted"):
            tool.deleted_at = tool.deleted_at or datetime.now(timezone.utc).replace(tzinfo=None)
            tool.plaza_status = "unlisted"
            tool.is_public = False
            tool.share_enabled = False
            hidden_tools += 1
    return disabled_users, hidden_tools


def seed_users(session) -> None:
    for data in DEMO_USERS:
        user = session.scalar(select(User).where(User.username == data["username"]))
        if user is None:
            user = User(username=data["username"])
            session.add(user)
        user.password_hash = hash_password(data["password"])
        user.role = data["role"]
        user.name = data["name"]
        user.school = data.get("school")
        user.subject = data.get("subject")
        user.grade = data.get("grade")
        user.is_active = True
        user.failed_login_attempts = 0
        user.locked_until = None


def seed_recommendation_rules(session) -> int:
    tools = {
        tool.name: tool
        for tool in session.scalars(select(Tool).where(Tool.is_preset.is_(True))).all()
    }
    created_or_updated = 0
    for subject, needs in SUBJECT_TOOL_MAP.items():
        category = SUBJECT_CATEGORY.get(subject)
        for need_type, names in needs.items():
            tool_ids = [str(tools[name].id) for name in names if name in tools]
            if not tool_ids:
                continue
            rule = session.scalar(
                select(RecommendRule).where(
                    RecommendRule.subject == subject,
                    RecommendRule.category == category,
                    RecommendRule.need_type == need_type,
                )
            )
            if rule is None:
                rule = RecommendRule(subject=subject, category=category, need_type=need_type)
                session.add(rule)
            rule.tool_ids = tool_ids
            rule.priority = 100
            rule.is_active = True
            created_or_updated += 1
    return created_or_updated


def seed_local_demo() -> None:
    with SessionLocal() as session:
        disabled_users, hidden_tools = hide_legacy_test_rows(session)
        if session.scalar(select(ToolTemplate.id).limit(1)) is None:
            insert_preset_templates(session)
        if session.scalar(select(Tool.id).where(Tool.is_preset.is_(True)).limit(1)) is None:
            insert_preset_tools(session)
        seed_users(session)
        rule_count = seed_recommendation_rules(session)
        session.commit()
        tool_count = session.query(Tool).filter(Tool.is_preset.is_(True)).count()

    print("本地演示数据已准备完成")
    print(f"预设工具：{tool_count} 个；推荐规则：{rule_count} 条")
    print(f"已停用历史测试账号：{disabled_users} 个；已隐藏历史测试工具：{hidden_tools} 个")
    print("教师：teacher_demo / Teacher2026")
    print("学生：student_demo / Student2026")
    print("管理员：admin_demo / Admin2026")


if __name__ == "__main__":
    seed_local_demo()
