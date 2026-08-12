from app.users.domain.repository import UserRepository
from app.users.domain.user import User


class ListUsers:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self) -> list[User]:
        return await self._repository.list_user()
