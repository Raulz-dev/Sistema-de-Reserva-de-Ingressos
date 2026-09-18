from uuid import uuid7

import pytest

from app.users.application.update_user import UpdateUser
from app.users.domain.enums import UserRole
from app.users.domain.exceptions import (
    UserEmailAlreadyExistsError,
    UserNotFoundError,
)
from app.users.domain.user import User


class FakeUserRepository:
    def __init__(self, users: list[User] | None = None) -> None:
        self.users = {user.id: user for user in users or []}

    async def find_by_id(self, user_id):
        user = self.users.get(user_id)
        return None if user is None else self._copy(user)

    async def find_by_email(self, email):
        user = next(
            (stored_user for stored_user in self.users.values() if stored_user.email == email),
            None,
        )
        return None if user is None else self._copy(user)

    async def update_user(self, user):
        self.users[user.id] = user
        return user

    @staticmethod
    def _copy(user: User) -> User:
        return User(
            id=user.id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
        )


@pytest.mark.asyncio
async def test_update_user_rejects_nonexistent_user() -> None:
    use_case = UpdateUser(FakeUserRepository())

    with pytest.raises(UserNotFoundError, match="Usuário não encontrado"):
        await use_case.execute(uuid7(), name="Novo Nome")


@pytest.mark.asyncio
async def test_update_user_rejects_email_used_by_another_user() -> None:
    user = User("Usuário Um", "user1@example.com", "hash", UserRole.USER)
    other_user = User("Usuário Dois", "user2@example.com", "hash", UserRole.USER)
    use_case = UpdateUser(FakeUserRepository([user, other_user]))

    with pytest.raises(UserEmailAlreadyExistsError, match="Email já cadastrado"):
        await use_case.execute(user.id, email=other_user.email)


@pytest.mark.asyncio
async def test_update_user_keeps_its_current_email() -> None:
    user = User("Usuário Um", "user1@example.com", "hash", UserRole.USER)
    use_case = UpdateUser(FakeUserRepository([user]))

    updated_user = await use_case.execute(user.id, email=user.email)

    assert updated_user.email == user.email
