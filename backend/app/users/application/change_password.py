from uuid import UUID

from app.security.password import PasswordHasher
from app.users.domain.exceptions import (
    InvalidUserEmailError,
    PasswordFail,
    UserDontExist,
)
from app.users.domain.repository import UserRepository
from app.users.domain.user import User


class ChangePassword:
    def __init__(self, repository: UserRepository, password_hasher: PasswordHasher):
        self._repository = repository
        self._password_hasher = password_hasher

    async def execute(
        self,
        user_id: UUID,
        email: str,
        new_password: str,
        new_password_confirmation: str,
    ) -> User:
        user = await self._repository.find_by_id(user_id)

        if user is None:
            raise UserDontExist("Usuário não encontrado!")

        if user.email != email:
            raise InvalidUserEmailError("E-mail ou credenciais inválidas.")

        if new_password != new_password_confirmation:
            raise PasswordFail("As senhas não coincidem!")

        password_hash = self._password_hasher.hash(new_password)

        user.change_password_hash(password_hash)

        return await self._repository.update_user(user)
