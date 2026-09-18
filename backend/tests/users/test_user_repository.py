from types import SimpleNamespace

import pytest
from sqlalchemy.exc import IntegrityError

from app.users.domain.exceptions import UserEmailAlreadyExistsError
from app.users.domain.user import User
from app.users.infrastructure.repository import SQLAlchemyUserRepository


class IntegrityErrorSession:
    def __init__(self, stored_user=None) -> None:
        self.stored_user = stored_user
        self.rollback_called = False

    def add(self, model) -> None:
        self.stored_user = model

    async def get(self, model_type, model_id):
        return self.stored_user

    async def commit(self) -> None:
        raise IntegrityError("statement", {}, Exception("duplicate email"))

    async def rollback(self) -> None:
        self.rollback_called = True


@pytest.mark.asyncio
async def test_create_user_translates_database_duplicate_to_domain_error() -> None:
    session = IntegrityErrorSession()
    repository = SQLAlchemyUserRepository(session)
    user = User("Usuário Teste", "user@example.com", "hash")

    with pytest.raises(UserEmailAlreadyExistsError, match="Email já cadastrado"):
        await repository.create_user(user)

    assert session.rollback_called is True


@pytest.mark.asyncio
async def test_update_user_translates_database_duplicate_to_domain_error() -> None:
    user = User("Usuário Teste", "user@example.com", "hash")
    stored_user = SimpleNamespace(
        id=user.id,
        name=user.name,
        email="existing@example.com",
        role=user.role,
        password_hash=user.password_hash,
    )
    session = IntegrityErrorSession(stored_user)
    repository = SQLAlchemyUserRepository(session)

    with pytest.raises(UserEmailAlreadyExistsError, match="Email já cadastrado"):
        await repository.update_user(user)

    assert session.rollback_called is True
