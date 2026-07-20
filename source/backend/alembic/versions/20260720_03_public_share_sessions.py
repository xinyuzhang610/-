"""Allow anonymous conversations from valid public share links.

Revision ID: 20260720_03
Revises: 20260715_02
Create Date: 2026-07-20
"""

from alembic import op
import sqlalchemy as sa


revision = "20260720_03"
down_revision = "20260715_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dialect = op.get_bind().dialect.name
    if dialect == "sqlite":
        with op.batch_alter_table("conversation_sessions") as batch:
            batch.alter_column(
                "user_id",
                existing_type=sa.Integer(),
                nullable=True,
            )
    else:
        op.alter_column(
            "conversation_sessions",
            "user_id",
            existing_type=sa.Integer(),
            nullable=True,
        )


def downgrade() -> None:
    dialect = op.get_bind().dialect.name
    if dialect == "sqlite":
        with op.batch_alter_table("conversation_sessions") as batch:
            batch.alter_column(
                "user_id",
                existing_type=sa.Integer(),
                nullable=False,
            )
    else:
        op.alter_column(
            "conversation_sessions",
            "user_id",
            existing_type=sa.Integer(),
            nullable=False,
        )
