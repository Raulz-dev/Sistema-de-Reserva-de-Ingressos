import pytest
from pydantic import ValidationError

from app.config.settings import Settings
from app.users.presentation.schemas import CreateUserRequest


def test_settings_are_safe_by_default() -> None:
    settings = Settings(
        database_url="postgresql+psycopg://user:password@localhost/database",
        jwt_secret="test-secret",
        token_expiration_minutes=60,
        algorithm="HS256",
        _env_file=None,
    )

    assert settings.debug is False
    assert settings.sql_echo is False


def test_registration_accepts_password_with_eight_characters() -> None:
    request = CreateUserRequest(
        name="Usuário Teste", email="user@example.com", password="12345678"
    )

    assert request.password == "12345678"


def test_registration_rejects_password_shorter_than_eight_characters() -> None:
    with pytest.raises(ValidationError):
        CreateUserRequest(
            name="Usuário Teste", email="user@example.com", password="1234567"
        )
