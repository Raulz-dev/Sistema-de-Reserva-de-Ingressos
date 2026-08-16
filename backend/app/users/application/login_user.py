from app.security.jwt import JWTService
from app.security.password import PasswordHasher
from app.users.domain.exceptions import InvalidCredentialsError
from app.users.domain.repository import UserRepository


class Login:
    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
        jwt_service: JWTService,
    ):
        self._repository = repository
        self._password_hasher = password_hasher
        self._jwt_service = jwt_service

    async def execute(self, email: str, password: str) -> str:
        user = await self._repository.find_by_email(email)

        if user is None:
            raise InvalidCredentialsError("Credenciais inválidas")

        verify_password = self._password_hasher.verify(
            password, user.password_hash
        )

        if not verify_password:
            raise InvalidCredentialsError("Credenciais inválidas")

        return self._jwt_service.create_token(user.id)
