from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.repository import UserRepository
from app.users.domain.user import User
from app.users.infrastructure.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_user(self, user: User) -> User:
        user_model = UserModel(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            password_hash=user.password_hash,
        )

        self._db.add(user_model)
        await self._db.commit()
        await self._db.refresh(user_model)

        return self._to_domain(user_model)

    async def find_by_id(self, user_id: UUID) -> User | None:
        user_model = await self._db.get(UserModel, user_id)

        if user_model is None:
            return None

        return self._to_domain(user_model)

    async def find_by_email(self, user_email: str) -> User | None:
        user = select(UserModel).where(UserModel.email == user_email)
        user_model = await self._db.scalar(user)

        if user_model is None:
            return None

        return self._to_domain(user_model)

    async def update_user(self, user: User) -> User | None:
        user_model = await self._db.get(UserModel, user.id)

        if user_model is None:
            return None

        user_model.name = user.name
        user_model.email = user.email
        user_model.role = user.role
        user_model.password_hash = user.password_hash

        await self._db.commit()
        await self._db.refresh(user_model)

        return self._to_domain(user_model)

    async def list_user(self) -> list[User] | None:
        all_users = select(UserModel).order_by(UserModel.name)
        result = await self._db.scalars(all_users)

        return [self._to_domain(users) for users in result.all()]

    def _to_domain(self, user: UserModel) -> User:
        return User(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            password_hash=user.password_hash,
        )
