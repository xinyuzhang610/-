from datetime import datetime, timedelta

from models.tool import Tool
from services.tool_access_service import can_view_public_share, public_tool_payload


def make_tool(**overrides):
    values = {
        "id": 9,
        "name": "私密课堂工具",
        "category": "文科",
        "prompt_template": "绝不能公开的提示词",
        "interface_config": {"internal": "secret"},
        "share_code": "share123",
        "share_enabled": True,
        "plaza_status": "unlisted",
    }
    values.update(overrides)
    return Tool(**values)


def test_public_share_payload_never_includes_internal_tool_configuration():
    payload = public_tool_payload(make_tool())

    assert payload["name"] == "私密课堂工具"
    assert "prompt_template" not in payload
    assert "interface_config" not in payload
    assert "creator_id" not in payload


def test_expired_or_deleted_share_cannot_be_viewed():
    assert can_view_public_share(make_tool())
    assert not can_view_public_share(make_tool(share_expires_at=datetime.utcnow() - timedelta(seconds=1)))
    assert not can_view_public_share(make_tool(deleted_at=datetime.utcnow()))
    assert not can_view_public_share(make_tool(share_enabled=False))
