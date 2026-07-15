"""Create the legacy 智教通 schema baseline.

Revision ID: 20260715_01
Revises:
Create Date: 2026-07-15
"""

from alembic import op
import sqlalchemy as sa


revision = "20260715_01"
down_revision = None
branch_labels = None
depends_on = None


category_enum = sa.Enum("文科", "理科", "通用", name="tool_category")
role_enum = sa.Enum("teacher", "student", "admin", name="user_role")


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=50), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", role_enum, nullable=False),
        sa.Column("name", sa.String(length=50)),
        sa.Column("school", sa.String(length=100)),
        sa.Column("subject", sa.String(length=50)),
        sa.Column("grade", sa.String(length=20)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_users_username", "users", ["username"])
    op.create_table(
        "tools",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("category", category_enum, nullable=False),
        sa.Column("subject", sa.String(length=50)),
        sa.Column("icon", sa.String(length=50)),
        sa.Column("prompt_template", sa.Text(), nullable=False),
        sa.Column("interface_config", sa.JSON()),
        sa.Column("creator_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("is_preset", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("is_public", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("share_code", sa.String(length=20), unique=True),
        sa.Column("usage_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_tools_share_code", "tools", ["share_code"])
    op.create_table(
        "tool_templates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("category", category_enum, nullable=False),
        sa.Column("subject", sa.String(length=50)),
        sa.Column("description", sa.Text()),
        sa.Column("prompt_template", sa.Text(), nullable=False),
        sa.Column("default_config", sa.JSON()),
        sa.Column("icon", sa.String(length=50)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_table(
        "usage_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("tool_id", sa.Integer(), sa.ForeignKey("tools.id"), nullable=False),
        sa.Column("input_text", sa.Text()),
        sa.Column("output_text", sa.Text()),
        sa.Column("session_id", sa.String(length=50)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_table(
        "favorites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("tool_id", sa.Integer(), sa.ForeignKey("tools.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("user_id", "tool_id", name="uq_user_tool"),
    )
    op.create_table(
        "recommend_rules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("subject", sa.String(length=50)),
        sa.Column("need_type", sa.String(length=50)),
        sa.Column("tool_ids", sa.JSON()),
        sa.Column("priority", sa.Integer(), server_default="0", nullable=False),
    )


def downgrade() -> None:
    op.drop_table("recommend_rules")
    op.drop_table("favorites")
    op.drop_table("usage_logs")
    op.drop_table("tool_templates")
    op.drop_index("ix_tools_share_code", table_name="tools")
    op.drop_table("tools")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
