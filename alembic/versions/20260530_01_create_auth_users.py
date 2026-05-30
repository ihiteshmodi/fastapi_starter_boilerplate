"""create auth users table

Revision ID: 20260530_01
Revises:
Create Date: 2026-05-30 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260530_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "auth_users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("password_hash", sa.String(length=128), nullable=False),
        sa.Column("scope", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )


def downgrade() -> None:
    op.drop_table("auth_users")
