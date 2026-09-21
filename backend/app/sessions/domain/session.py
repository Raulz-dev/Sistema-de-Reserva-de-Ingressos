from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid7

from app.sessions.domain.exceptions import InvalidSessionError


@dataclass
class Session:
    movie_id: UUID
    room_id: UUID
    starts_at: datetime
    ends_at: datetime
    price: Decimal
    is_active: bool = True
    id: UUID = field(default_factory=uuid7)

    def __post_init__(self) -> None:
        self._validate_period(self.starts_at, self.ends_at)
        self.price = self._validate_price(self.price)
        if not isinstance(self.is_active, bool):
            raise InvalidSessionError("O status deve ser verdadeiro ou falso.")

    def change_movie(self, movie_id: UUID) -> None:
        self.movie_id = movie_id

    def change_room(self, room_id: UUID) -> None:
        self.room_id = room_id

    def change_period(self, starts_at: datetime, ends_at: datetime) -> None:
        self._validate_period(starts_at, ends_at)
        self.starts_at = starts_at
        self.ends_at = ends_at

    def change_price(self, price: Decimal) -> None:
        self.price = self._validate_price(price)

    def deactivate(self) -> None:
        self.is_active = False

    @staticmethod
    def _validate_period(starts_at: datetime, ends_at: datetime) -> None:
        if starts_at.tzinfo is None or starts_at.utcoffset() is None:
            raise InvalidSessionError("O início da sessão deve informar o fuso horário.")
        if ends_at.tzinfo is None or ends_at.utcoffset() is None:
            raise InvalidSessionError("O término da sessão deve informar o fuso horário.")
        if ends_at <= starts_at:
            raise InvalidSessionError("O término deve ser posterior ao início da sessão.")

    @staticmethod
    def _validate_price(price: Decimal) -> Decimal:
        price = Decimal(price)
        if price <= 0:
            raise InvalidSessionError("O preço deve ser maior que zero.")
        return price
