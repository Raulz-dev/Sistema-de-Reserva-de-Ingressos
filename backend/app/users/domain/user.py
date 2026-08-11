from dataclasses import dataclass, field
from uuid import UUID, uuid7

from email_validator import EmailNotValidError, validate_email

from app.users.domain.enums import UserRole
from app.users.domain.exceptions import (
    InvalidUserEmailError,
    InvalidUserNameError,
    InvalidUserPasswordHashError,
    InvalidUserRoleError,
)


@dataclass(slots=True)
class User:
    name: str
    email: str
    password_hash: str
    role: UserRole = UserRole.USER
    id: UUID = field(default_factory=uuid7)

    def __post_init__(self) -> None:
        self.name = self._validate_name(self.name)
        self.email = self._validate_email(self.email)
        self.password_hash = self._validate_password_hash(self.password_hash)
        self.role = self._validate_role(self.role)

    def change_name(self, new_name: str) -> None:
        self.name = self._validate_name(new_name)

    def change_email(self, new_email: str) -> None:
        self.email = self._validate_email(new_email)

    def change_password_hash(self, new_password_hash: str) -> None:
        self.password_hash = self._validate_password_hash(new_password_hash)

    def change_role(self, new_role: UserRole) -> None:
        self.role = self._validate_role(new_role)

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str):
            raise InvalidUserNameError("O nome deve ser do tipo string.")

        normalized_name = name.strip()

        if len(normalized_name) < 2:
            raise InvalidUserNameError("O nome deve ter no mínimo dois caracteres.")

        if any(character.isdigit() for character in normalized_name):
            raise InvalidUserNameError("O nome não pode conter números.")

        return normalized_name

    @staticmethod
    def _validate_email(email: str) -> str:
        if not isinstance(email, str):
            raise InvalidUserEmailError("O email deve ser do tipo string.")

        try:
            validated_email = validate_email(email, check_deliverability=False)

        except EmailNotValidError as error:
            raise InvalidUserEmailError("O email informado é invalido.") from error

        return validated_email.normalized

    @staticmethod
    def _validate_password_hash(password_hash: str) -> str:
        if not isinstance(password_hash, str):
            raise InvalidUserPasswordHashError("A senha deve ser do tipo string")
        if len(password_hash) < 1:
            raise InvalidUserPasswordHashError("A senha não pode ser vazia.")

        return password_hash

    @staticmethod
    def _validate_role(role: UserRole) -> UserRole:
        if not isinstance(role, UserRole):
            raise InvalidUserRoleError("O perfil do usuário é invalido.")

        return role
