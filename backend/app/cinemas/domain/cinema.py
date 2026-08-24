from dataclasses import dataclass, field
from uuid import UUID, uuid7

from app.cinemas.domain.exceptions import InvalidCinemaError


@dataclass(slots=True)
class Cinema:
    name: str
    street: str
    number: str
    neighborhood: str
    zip_code: str
    complement: str | None = None
    is_active: bool = True
    id: UUID = field(default_factory=uuid7)

    def __post_init__(self) -> None:
        self.name = self._required_text(self.name, "nome")
        self.street = self._required_text(self.street, "logradouro")
        self.number = self._required_text(self.number, "número")
        self.neighborhood = self._required_text(self.neighborhood, "bairro")
        self.zip_code = self._validate_zip_code(self.zip_code)
        self.complement = self._optional_text(self.complement)
        self.is_active = self._validate_is_active(self.is_active)

    def change_name(self, value: str) -> None:
        self.name = self._required_text(value, "nome")

    def change_street(self, value: str) -> None:
        self.street = self._required_text(value, "logradouro")

    def change_number(self, value: str) -> None:
        self.number = self._required_text(value, "número")

    def change_complement(self, value: str | None) -> None:
        self.complement = self._optional_text(value)

    def change_neighborhood(self, value: str) -> None:
        self.neighborhood = self._required_text(value, "bairro")

    def change_zip_code(self, value: str) -> None:
        self.zip_code = self._validate_zip_code(value)

    def deactivate(self) -> None:
        self.is_active = False

    @staticmethod
    def _required_text(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise InvalidCinemaError(f"O campo {field_name} é obrigatório.")
        return value.strip()

    @staticmethod
    def _optional_text(value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise InvalidCinemaError("O complemento deve ser um texto.")
        return value.strip() or None

    @staticmethod
    def _validate_zip_code(value: str) -> str:
        if not isinstance(value, str):
            raise InvalidCinemaError("O CEP deve conter 8 dígitos.")
        normalized = "".join(character for character in value if character.isdigit())
        if len(normalized) != 8:
            raise InvalidCinemaError("O CEP deve conter 8 dígitos.")
        return normalized

    @staticmethod
    def _validate_is_active(value: bool) -> bool:
        if not isinstance(value, bool):
            raise InvalidCinemaError("O status deve ser verdadeiro ou falso.")
        return value
