from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, IdMixin, TimestampMixin


class MovieModel(Base, IdMixin, TimestampMixin):
    __tablename__ = "movie"

    title: Mapped[str] = mapped_column(nullable=False)
    synopsis: Mapped[str] = mapped_column(nullable=False)
    age_rating: Mapped[str] = mapped_column(nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(nullable=False)
    trailer_url: Mapped[str] = mapped_column(nullable=True)

    def __str__(self) -> str:
        return self.title
