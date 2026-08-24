"""create cinemas and rooms tables

Revision ID: c8a2f7d1e4b0
Revises: befc0d3defc2
Create Date: 2026-08-24 00:00:00.000000

"""
from typing import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "c8a2f7d1e4b0"
down_revision: str | Sequence[str] | None = "befc0d3defc2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "cinemas",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("street", sa.String(), nullable=False),
        sa.Column("number", sa.String(), nullable=False),
        sa.Column("complement", sa.String(), nullable=True),
        sa.Column("neighborhood", sa.String(), nullable=False),
        sa.Column("zip_code", sa.String(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "rooms",
        sa.Column("cinema_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("seats_per_row", sa.Integer(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.ForeignKeyConstraint(["cinema_id"], ["cinemas.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cinema_id", "name", name="uq_rooms_cinema_name"),
    )


def downgrade() -> None:
    op.drop_table("rooms")
    op.drop_table("cinemas")
