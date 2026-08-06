from typing import Protocol
from uuid import UUID

from app.users.domain.user import User


class UserRepository(Protocol):
    async def add_user(self, user: User) -> None: ...

    async def get_id_user(self, user_id: UUID) -> None: ...

    async def get_email_user(self, user_email: str) -> None: ...

    async def update_user(self, user_id: UUID, user: User) -> None: ...
