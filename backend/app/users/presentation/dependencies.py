from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.database.session import get_db
from app.security.jwt import JWTService
from app.security.password import PasswordHasher
from app.users.application.change_password import ChangePassword
from app.users.application.create_user import CreateUser
from app.users.application.get_user_by_id import GetUserById
from app.users.application.list_all_users import ListUsers
from app.users.application.login_user import Login
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


def get_change_password(db: Annotated[AsyncSession, Depends(get_db)]) -> ChangePassword:
    repository = SQLAlchemyUserRepository(db)
    password_hasher = PasswordHasher()

    return ChangePassword(repository, password_hasher)


def get_login_user(db: Annotated[AsyncSession, Depends(get_db)]) -> Login:

    repository = SQLAlchemyUserRepository(db)
    password_hasher = PasswordHasher()

    jwt_service = JWTService(
        secret_key=settings.jwt_secret,
        expiration_minutes=settings.token_expiration_minutes,
        algorithm=settings.algorithm,
    )
    return Login(
        repository=repository, password_hasher=password_hasher, jwt_service=jwt_service
    )
