from datetime import datetime

from fastapi import HTTPException, status

from models.tool import Tool
from models.user import User


PUBLIC_TOOL_FIELDS = ("id", "name", "description", "category", "subject", "icon", "share_code", "usage_count", "created_at", "updated_at")


def is_plaza_visible(tool: Tool) -> bool:
    return tool.deleted_at is None and tool.plaza_status == "published"


def can_view_public_share(tool: Tool, now: datetime | None = None) -> bool:
    current_time = now or datetime.utcnow()
    return bool(
        tool.deleted_at is None
        and tool.share_enabled
        and tool.share_code
        and (tool.share_expires_at is None or tool.share_expires_at > current_time)
    )


def public_tool_payload(tool: Tool) -> dict:
    return {field: getattr(tool, field) for field in PUBLIC_TOOL_FIELDS}


def can_manage_tool(user: User, tool: Tool) -> bool:
    return user.role == "admin" or tool.creator_id == user.id


def assert_tool_manager(user: User, tool: Tool) -> None:
    if not can_manage_tool(user, tool):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只能操作自己的工具")


def assert_tool_can_be_used(user: User, tool: Tool) -> None:
    if tool.deleted_at is not None:
        raise HTTPException(status_code=404, detail="工具不存在")
    if user.role == "admin" or tool.creator_id == user.id:
        return
    if not is_plaza_visible(tool):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权使用该工具")
