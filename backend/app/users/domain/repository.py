from typing import Protocol
from uuid import UUID

from app.users.domain.user import User


class UserRepository(Protocol):
    async def create_user(self, user: User) -> None: ...

    async def find_by_id(self, user_id: UUID) -> None: ...

    async def find_by_email(self, user_email: str) -> None: ...

    async def update_user(self, user_id: UUID, user: User) -> None: ...
