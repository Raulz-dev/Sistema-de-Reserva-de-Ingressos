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


def get_jwt_service() -> JWTService:
    return JWTService(
        secret_key=settings.jwt_secret,
        expiration_minutes=settings.token_expiration_minutes,
        algorithm=settings.algorithm,
    )


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
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

    repository = SQLAlchemyUserRepository(db)
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

    jwt_service = get_jwt_service()
    return Login(
        repository=repository, password_hasher=password_hasher, jwt_service=jwt_service
    )
