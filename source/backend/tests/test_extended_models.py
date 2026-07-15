from models.audit import AuditLog
from models.conversation import ConversationMessage, ConversationSession
from models.session import AuthSession
from models.tool import Tool
from models.usage import UsageLog
from models.user import User


def column_names(model):
    return set(model.__table__.columns.keys())


def test_user_security_state_is_persisted():
    columns = column_names(User)
    assert {"is_active", "failed_login_attempts", "locked_until", "last_login_at", "password_changed_at", "token_version"} <= columns


def test_tool_lifecycle_state_is_persisted():
    columns = column_names(Tool)
    assert {"template_source_id", "source_type", "deleted_at", "plaza_status", "share_enabled", "share_expires_at", "external_platform_url"} <= columns


def test_sessions_conversations_and_audits_have_models():
    assert {"jti", "user_id", "last_seen_at", "expires_at", "revoked_at"} <= column_names(AuthSession)
    assert {"id", "user_id", "tool_id", "last_activity_at"} <= column_names(ConversationSession)
    assert {"session_id", "role", "content"} <= column_names(ConversationMessage)
    assert {"actor_id", "action", "resource_type", "resource_id", "details"} <= column_names(AuditLog)


def test_usage_can_represent_general_and_interrupted_conversations():
    columns = column_names(UsageLog)
    assert UsageLog.__table__.columns["tool_id"].nullable
    assert {"status", "latency_ms", "completed_at"} <= columns
