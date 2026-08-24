from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, IdMixin, IsActiveMixin, TimestampMixin


class CinemaModel(Base, IdMixin, TimestampMixin, IsActiveMixin):
    __tablename__ = "cinemas"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    street: Mapped[str] = mapped_column(nullable=False)
    number: Mapped[str] = mapped_column(nullable=False)
    complement: Mapped[str | None] = mapped_column(nullable=True)
    neighborhood: Mapped[str] = mapped_column(nullable=False)
    zip_code: Mapped[str] = mapped_column(nullable=False)

    def __str__(self) -> str:
        return self.name


class RoomModel(Base, IdMixin, TimestampMixin, IsActiveMixin):
    __tablename__ = "rooms"
    __table_args__ = (UniqueConstraint("cinema_id", "name", name="uq_rooms_cinema_name"),)

    cinema_id: Mapped[UUID] = mapped_column(ForeignKey("cinemas.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    row_count: Mapped[int] = mapped_column(nullable=False)
    seats_per_row: Mapped[int] = mapped_column(nullable=False)

    def __str__(self) -> str:
        return self.name
