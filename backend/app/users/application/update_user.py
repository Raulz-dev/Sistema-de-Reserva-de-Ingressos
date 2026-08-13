from uuid import UUID

from app.users.domain.enums import UserRole
from app.users.domain.exceptions import UserDontExist
from app.users.domain.repository import UserRepository
from app.users.domain.user import User


class UpdateUser:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(
        self,
        user_id: UUID,
        name: str | None = None,
        email: str | None = None,
        role: UserRole | None = None,
    ) -> User:
        user = await self._repository.find_by_id(user_id)

        if user is None:
            raise UserDontExist("Usuário não encontrado!")

        if name is not None:
            user.change_name(name)

        if email is not None:
            user.change_email(email)

        if role is not None:
            user.change_role(role)

        return await self._repository.update_user(user)
