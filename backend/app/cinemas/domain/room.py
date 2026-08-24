from dataclasses import dataclass, field
from uuid import UUID, uuid7

from app.cinemas.domain.exceptions import InvalidRoomError


@dataclass(slots=True)
class Room:
    cinema_id: UUID
    name: str
    row_count: int
    seats_per_row: int
    is_active: bool = True
    id: UUID = field(default_factory=uuid7)

    def __post_init__(self) -> None:
        if not isinstance(self.cinema_id, UUID):
            raise InvalidRoomError("O cinema da sala é inválido.")
        self.name = self._validate_name(self.name)
        self.row_count = self._validate_positive_integer(self.row_count, "linhas")
        self.seats_per_row = self._validate_positive_integer(
            self.seats_per_row, "assentos por linha"
        )
        self.is_active = self._validate_is_active(self.is_active)

    @property
    def capacity(self) -> int:
        return self.row_count * self.seats_per_row

    def change_name(self, value: str) -> None:
        self.name = self._validate_name(value)

    def change_row_count(self, value: int) -> None:
        self.row_count = self._validate_positive_integer(value, "linhas")

    def change_seats_per_row(self, value: int) -> None:
        self.seats_per_row = self._validate_positive_integer(
            value, "assentos por linha"
        )

    def deactivate(self) -> None:
        self.is_active = False

    @staticmethod
    def _validate_name(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise InvalidRoomError("O campo nome é obrigatório.")
        return value.strip()

    @staticmethod
    def _validate_positive_integer(value: int, field_name: str) -> int:
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise InvalidRoomError(
                f"O campo {field_name} deve ser um número inteiro positivo."
            )
        return value

    @staticmethod
    def _validate_is_active(value: bool) -> bool:
        if not isinstance(value, bool):
            raise InvalidRoomError("O status deve ser verdadeiro ou falso.")
        return value
