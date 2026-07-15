"""Add secure lifecycle, conversation, and administration schema.

Revision ID: 20260715_02
Revises: 20260715_01
Create Date: 2026-07-15
"""

from alembic import op
import sqlalchemy as sa


revision = "20260715_02"
down_revision = "20260715_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column("users", sa.Column("failed_login_attempts", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("users", sa.Column("locked_until", sa.DateTime(), nullable=True))
    op.add_column("users", sa.Column("last_login_at", sa.DateTime(), nullable=True))
    op.add_column("users", sa.Column("password_changed_at", sa.DateTime(), nullable=True))
    op.add_column("users", sa.Column("token_version", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("users", sa.Column("updated_at", sa.DateTime(), nullable=True))
    op.create_index("ix_users_active_role", "users", ["is_active", "role"])

    op.add_column("tools", sa.Column("template_source_id", sa.Integer(), nullable=True))
    op.add_column("tools", sa.Column("source_type", sa.String(length=20), nullable=False, server_default="manual"))
    op.add_column("tools", sa.Column("deleted_at", sa.DateTime(), nullable=True))
    op.add_column("tools", sa.Column("plaza_status", sa.String(length=20), nullable=False, server_default="published"))
    op.add_column("tools", sa.Column("share_enabled", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column("tools", sa.Column("share_expires_at", sa.DateTime(), nullable=True))
    op.add_column("tools", sa.Column("external_platform_url", sa.String(length=500), nullable=True))
    op.execute("UPDATE tools SET plaza_status = CASE WHEN is_public = 1 THEN 'published' ELSE 'unlisted' END")
    op.execute("UPDATE tools SET share_enabled = is_public")
    op.create_index("ix_tools_creator_lifecycle", "tools", ["creator_id", "deleted_at", "updated_at"])
    op.create_index("ix_tools_plaza_lifecycle", "tools", ["plaza_status", "deleted_at", "created_at"])
    op.create_index("ix_tools_share_lifecycle", "tools", ["share_code", "share_enabled", "share_expires_at"])

    dialect = op.get_bind().dialect.name
    if dialect == "sqlite":
        with op.batch_alter_table("usage_logs") as batch:
            batch.alter_column("tool_id", existing_type=sa.Integer(), nullable=True)
    else:
        op.alter_column("usage_logs", "tool_id", existing_type=sa.Integer(), nullable=True)
    op.add_column("usage_logs", sa.Column("status", sa.String(length=20), nullable=False, server_default="completed"))
    op.add_column("usage_logs", sa.Column("latency_ms", sa.Integer(), nullable=True))
    op.add_column("usage_logs", sa.Column("completed_at", sa.DateTime(), nullable=True))
    op.create_index("ix_usage_tool_created", "usage_logs", ["tool_id", "created_at"])
    op.create_index("ix_usage_user_created", "usage_logs", ["user_id", "created_at"])
    op.create_index("ix_usage_session", "usage_logs", ["session_id", "created_at"])

    op.add_column("recommend_rules", sa.Column("category", sa.String(length=20), nullable=True))
    op.add_column("recommend_rules", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column("recommend_rules", sa.Column("created_at", sa.DateTime(), nullable=True))
    op.add_column("recommend_rules", sa.Column("updated_at", sa.DateTime(), nullable=True))
    op.create_index("ix_rules_matching", "recommend_rules", ["is_active", "subject", "category", "need_type", "priority"])
    op.create_index("ix_favorites_user_created", "favorites", ["user_id", "created_at"])

    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("jti", sa.String(length=64), nullable=False, unique=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("issued_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("last_seen_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(), nullable=True),
        sa.Column("revoke_reason", sa.String(length=100), nullable=True),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("user_agent", sa.String(length=500), nullable=True),
    )
    op.create_index("ix_auth_sessions_user_active", "auth_sessions", ["user_id", "revoked_at", "expires_at"])

    op.create_table(
        "conversation_sessions",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("tool_id", sa.Integer(), sa.ForeignKey("tools.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("last_activity_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_conversation_owner_activity", "conversation_sessions", ["user_id", "last_activity_at"])
    op.create_table(
        "conversation_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("session_id", sa.String(length=64), sa.ForeignKey("conversation_sessions.id"), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_conversation_messages_order", "conversation_messages", ["session_id", "created_at"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action", sa.String(length=80), nullable=False),
        sa.Column("resource_type", sa.String(length=80), nullable=False),
        sa.Column("resource_id", sa.String(length=80), nullable=True),
        sa.Column("result", sa.String(length=20), nullable=False, server_default="success"),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("user_agent", sa.String(length=500), nullable=True),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_audit_filter", "audit_logs", ["created_at", "actor_id", "action"])


def downgrade() -> None:
    op.drop_index("ix_audit_filter", table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index("ix_conversation_messages_order", table_name="conversation_messages")
    op.drop_table("conversation_messages")
    op.drop_index("ix_conversation_owner_activity", table_name="conversation_sessions")
    op.drop_table("conversation_sessions")
    op.drop_index("ix_auth_sessions_user_active", table_name="auth_sessions")
    op.drop_table("auth_sessions")
    op.drop_index("ix_favorites_user_created", table_name="favorites")
    op.drop_index("ix_rules_matching", table_name="recommend_rules")
    for column in ("updated_at", "created_at", "is_active", "category"):
        op.drop_column("recommend_rules", column)
    for column in ("completed_at", "latency_ms", "status"):
        op.drop_column("usage_logs", column)
    dialect = op.get_bind().dialect.name
    if dialect == "sqlite":
        with op.batch_alter_table("usage_logs") as batch:
            batch.alter_column("tool_id", existing_type=sa.Integer(), nullable=False)
    else:
        op.alter_column("usage_logs", "tool_id", existing_type=sa.Integer(), nullable=False)
    for index in ("ix_usage_session", "ix_usage_user_created", "ix_usage_tool_created"):
        op.drop_index(index, table_name="usage_logs")
    for index in ("ix_tools_share_lifecycle", "ix_tools_plaza_lifecycle", "ix_tools_creator_lifecycle"):
        op.drop_index(index, table_name="tools")
    for column in ("external_platform_url", "share_expires_at", "share_enabled", "plaza_status", "deleted_at", "source_type", "template_source_id"):
        op.drop_column("tools", column)
    op.drop_index("ix_users_active_role", table_name="users")
    for column in ("updated_at", "token_version", "password_changed_at", "last_login_at", "locked_until", "failed_login_attempts", "is_active"):
        op.drop_column("users", column)
