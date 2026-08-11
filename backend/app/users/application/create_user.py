from app.security.password import PasswordHasher
from app.users.domain.enums import UserRole
from app.users.domain.exceptions import (
    InvalidUserRoleError,
    UserEmailAlreadyExistsError,
)
from app.users.domain.repository import UserRepository
from app.users.domain.user import User


class CreateUser:
    def __init__(self, repository: UserRepository, password_hasher: PasswordHasher):
        self._repository = repository
        self._password_hasher = password_hasher

    async def execute(
        self, name: str, email: str, password: str, role: UserRole = UserRole.USER
    ) -> User:
        email_exist = await self._repository.find_by_email(email)
        if email_exist:
            raise UserEmailAlreadyExistsError("Email já cadastrado!")

        if not isinstance(role, UserRole):
            raise InvalidUserRoleError("Cargo não válido!")

        password_hash = self._password_hasher.hash(password)

        user = User(name, email, password_hash=password_hash, role=role)

        return await self._repository.create_user(user)
