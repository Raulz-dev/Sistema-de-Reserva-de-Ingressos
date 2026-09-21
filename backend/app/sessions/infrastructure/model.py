from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, IdMixin, IsActiveMixin, TimestampMixin


class SessionModel(Base, IdMixin, TimestampMixin, IsActiveMixin):
    __tablename__ = "sessions"
    __table_args__ = (
        Index("ix_sessions_room_period", "room_id", "starts_at", "ends_at"),
    )

    movie_id: Mapped[UUID] = mapped_column(ForeignKey("movie.id"), nullable=False)
    room_id: Mapped[UUID] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
