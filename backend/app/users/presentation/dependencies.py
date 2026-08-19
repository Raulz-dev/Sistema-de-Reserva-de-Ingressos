from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
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
from app.users.domain.enums import UserRole
from app.users.domain.user import User
from app.users.infrastructure.repository import SQLAlchemyUserRepository

bearer_scheme = HTTPBearer(auto_error=False)


def get_user_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)


def get_jwt_service() -> JWTService:
    return JWTService(
        secret_key=settings.jwt_secret,
        expiration_minutes=settings.token_expiration_minutes,
        algorithm=settings.algorithm,
    )


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    repository: Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)],
    jwt_service: Annotated[JWTService, Depends(get_jwt_service)],
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise unauthorized

    try:
        payload = jwt_service.decode_token(credentials.credentials)
        subject = payload.get("sub")
        if not isinstance(subject, str):
            raise ValueError
        user_id = UUID(subject)
    except ValueError as error:
        raise unauthorized from error

    user = await repository.find_by_id(user_id)

    if user is None:
        raise unauthorized

    return user


async def require_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido apenas para administradores",
        )

    return current_user


def get_create_user(
    repository: Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)],
) -> CreateUser:
    password_hasher = PasswordHasher()

    return CreateUser(
        repository=repository,
        password_hasher=password_hasher,
    )


def get_list_all_user(
    repository: Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)],
) -> ListUsers:
    return ListUsers(repository)


def get_update_user(
    repository: Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)],
) -> UpdateUser:
    return UpdateUser(repository)


def get_user_by_id(
    repository: Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)],
) -> GetUserById:
    return GetUserById(repository)


def get_change_password(
    repository: Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)],
) -> ChangePassword:
    password_hasher = PasswordHasher()

    return ChangePassword(repository, password_hasher)


def get_login_user(
    repository: Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)],
) -> Login:
    password_hasher = PasswordHasher()

    jwt_service = get_jwt_service()
    return Login(
        repository=repository, password_hasher=password_hasher, jwt_service=jwt_service
    )
