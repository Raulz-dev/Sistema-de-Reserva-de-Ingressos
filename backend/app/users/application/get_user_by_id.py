from uuid import UUID

from app.users.domain.exceptions import UserNotFoundError
from app.users.domain.repository import UserRepository
from app.users.domain.user import User


class GetUserById:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, user_id: UUID) -> User:
        user = await self._repository.find_by_id(user_id)

        if user is None:
            raise UserNotFoundError("Usuário não encontrado.")
        print("PRINT PRINT PRINT PRINT", user)
        return user
