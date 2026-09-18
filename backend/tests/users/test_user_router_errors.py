from uuid import uuid7

import pytest
from fastapi import HTTPException

from app.users.domain.enums import UserRole
from app.users.domain.exceptions import (
    InvalidCredentialsError,
    PasswordMismatchError,
    UserEmailAlreadyExistsError,
    UserNotFoundError,
)
from app.users.domain.user import User
from app.users.presentation.router import change_password, get_user, update_user
from app.users.presentation.schemas import ChangePasswordRequest, UpdateUserRequest


class RaisingUseCase:
    def __init__(self, error: Exception) -> None:
        self.error = error

    async def execute(self, *args, **kwargs):
        raise self.error


def make_user() -> User:
    return User("Usuário Teste", "user@example.com", "hash", UserRole.USER)


@pytest.mark.asyncio
async def test_get_user_maps_not_found_to_404() -> None:
    current_user = make_user()

    with pytest.raises(HTTPException) as captured:
        await get_user(
            current_user.id,
            RaisingUseCase(UserNotFoundError("Usuário não encontrado.")),
            current_user,
        )

    assert captured.value.status_code == 404


@pytest.mark.asyncio
async def test_update_user_maps_not_found_to_404() -> None:
    with pytest.raises(HTTPException) as captured:
        await update_user(
            uuid7(),
            UpdateUserRequest(name="Novo Nome"),
            RaisingUseCase(UserNotFoundError("Usuário não encontrado.")),
            make_user(),
        )

    assert captured.value.status_code == 404


@pytest.mark.asyncio
async def test_update_user_maps_duplicate_email_to_409() -> None:
    with pytest.raises(HTTPException) as captured:
        await update_user(
            uuid7(),
            UpdateUserRequest(name="Novo Nome", email="used@example.com"),
            RaisingUseCase(UserEmailAlreadyExistsError("Email já cadastrado!")),
            make_user(),
        )

    assert captured.value.status_code == 409


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "error",
    [
        InvalidCredentialsError("E-mail ou credenciais inválidas."),
        PasswordMismatchError("As senhas não coincidem."),
    ],
)
async def test_change_password_maps_invalid_request_to_400(error: Exception) -> None:
    current_user = make_user()
    request = ChangePasswordRequest(
        email=current_user.email,
        new_password="novaSenha123",
        new_password_confirmation="novaSenha123",
    )

    with pytest.raises(HTTPException) as captured:
        await change_password(
            current_user.id,
            request,
            RaisingUseCase(error),
            current_user,
        )

    assert captured.value.status_code == 400


@pytest.mark.asyncio
async def test_change_password_maps_not_found_to_404() -> None:
    current_user = make_user()
    request = ChangePasswordRequest(
        email=current_user.email,
        new_password="novaSenha123",
        new_password_confirmation="novaSenha123",
    )

    with pytest.raises(HTTPException) as captured:
        await change_password(
            current_user.id,
            request,
            RaisingUseCase(UserNotFoundError("Usuário não encontrado.")),
            current_user,
        )

    assert captured.value.status_code == 404
