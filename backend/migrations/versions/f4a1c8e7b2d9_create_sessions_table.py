"""create sessions table

Revision ID: f4a1c8e7b2d9
Revises: e2b7c9d4a6f1
Create Date: 2026-09-18 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f4a1c8e7b2d9"
down_revision: str | Sequence[str] | None = "e2b7c9d4a6f1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "sessions",
        sa.Column("movie_id", sa.Uuid(), nullable=False),
        sa.Column("room_id", sa.Uuid(), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.CheckConstraint("ends_at > starts_at", name="ck_sessions_valid_period"),
        sa.CheckConstraint("price > 0", name="ck_sessions_positive_price"),
        sa.ForeignKeyConstraint(["movie_id"], ["movie.id"]),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_sessions_room_period", "sessions", ["room_id", "starts_at", "ends_at"]
    )


def downgrade() -> None:
    op.drop_index("ix_sessions_room_period", table_name="sessions")
    op.drop_table("sessions")
