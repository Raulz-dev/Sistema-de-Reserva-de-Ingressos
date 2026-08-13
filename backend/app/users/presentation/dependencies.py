from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.security.password import PasswordHasher
from app.users.application.create_user import CreateUser
from app.users.application.get_user_by_id import GetUserById
from app.users.application.list_all_users import ListUsers
from app.users.application.update_user import UpdateUser
from app.users.infrastructure.repository import SQLAlchemyUserRepository


def get_create_user(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CreateUser:
    repository = SQLAlchemyUserRepository(db)
    password_hasher = PasswordHasher()

    return CreateUser(
        repository=repository,
        password_hasher=password_hasher,
    )


def get_list_all_user(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ListUsers:
    repository = SQLAlchemyUserRepository(db)

    return ListUsers(repository)


def get_update_user(db: Annotated[AsyncSession, Depends(get_db)]) -> UpdateUser:
    repository = SQLAlchemyUserRepository(db)

    return UpdateUser(repository)


def get_user_by_id(db: Annotated[AsyncSession, Depends(get_db)]) -> GetUserById:
    repository = SQLAlchemyUserRepository(db)

    return GetUserById(repository)
