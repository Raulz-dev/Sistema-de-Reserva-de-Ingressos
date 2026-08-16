from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError


class JWTService:
    def __init__(
        self, secret_key: str, expiration_minutes: int, algorithm: str
    ) -> None:
        self._secret_key = secret_key
        self._expiration_minutes = expiration_minutes
        self._algorithm = algorithm

    def create_token(self, user_id: UUID) -> str:
        expiration_time = datetime.now(timezone.utc) + timedelta(
            minutes=self._expiration_minutes
        )
        dic_info = {
            "sub": str(user_id),
            "exp": expiration_time,
            "iat": datetime.now(timezone.utc),
        }

        return jwt.encode(dic_info, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        except InvalidTokenError as error:
            raise ValueError("Token inválido ou expirado") from error
