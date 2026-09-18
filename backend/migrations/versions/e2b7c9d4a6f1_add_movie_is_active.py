"""add movie is active

Revision ID: e2b7c9d4a6f1
Revises: c8a2f7d1e4b0
Create Date: 2026-09-18 00:00:00.000000

"""
from typing import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "e2b7c9d4a6f1"
down_revision: str | Sequence[str] | None = "c8a2f7d1e4b0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "movie",
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("movie", "is_active")
