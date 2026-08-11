from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.domain.repository import UserRepository
from app.users.domain.user import User
from app.users.infrastructure.models import UserModel


class sqlalchemyUserRepository(UserRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_user(self, user: User) -> User:
        user_model = (
            UserModel(
                id=user.id,
                name=user.name,
                email=user.email,
                role=user.role,
                password_hash=self.password_hash,
            ),
        )

        self._db.add(user_model)
        await self._db.commit()
        await self._db.refresh(user_model)

        return await self._to_domain(user_model)

    async def find_by_id(self, user_id: UUID) -> User | None:
        userExist = await self.db.get(UserModel, user_id)

        if userExist is None:
            return None

        return await self._to_domain(userExist)

    async def find_by_email(self, user_email: str) -> User | None:
        user = select(UserModel).where(UserModel.email == user_email)

        user_model = await self.db.scalar(user)

        if user_model is None:
            return None

        return self._to_domain(user_model)

    async def update_user(self, user_id: UUID, user) -> User | None:
        user_model = await self.db.get(UserModel, user_id)

        if user is None:
            return None

        user_model.name = user.name
        user_model.email = user.email
        user_model.role = user.role
        user_model.password_hash = user.password_hash

        await self.db.commit()
        await self.db.refresh(user_model)

        return await self._to_domain(user_model)

    def _to_domain(user: UserModel) -> User:
        return User(id=user.id, name=user.name, email=user.email, role=user.role)
