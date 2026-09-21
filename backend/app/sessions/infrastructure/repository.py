from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.sessions.domain.repository import SessionRepository
from app.sessions.domain.session import Session
from app.sessions.infrastructure.model import SessionModel


class SQLAlchemySessionRepository(SessionRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_session(self, session: Session) -> Session:
        model = self._to_model(session)
        self._db.add(model)
        await self._db.commit()
        await self._db.refresh(model)
        return self._to_domain(model)

    async def find_session_by_id(self, session_id: UUID) -> Session | None:
        model = await self._db.scalar(
            select(SessionModel).where(
                SessionModel.id == session_id, SessionModel.is_active.is_(True)
            )
        )
        return None if model is None else self._to_domain(model)

    async def list_sessions(self) -> list[Session]:
        result = await self._db.scalars(
            select(SessionModel)
            .where(SessionModel.is_active.is_(True))
            .order_by(SessionModel.starts_at)
        )
        return [self._to_domain(model) for model in result.all()]

    async def has_room_conflict(
        self,
        room_id: UUID,
        starts_at: datetime,
        ends_at: datetime,
        exclude_session_id: UUID | None = None,
    ) -> bool:
        query = select(SessionModel.id).where(
            SessionModel.room_id == room_id,
            SessionModel.is_active.is_(True),
            SessionModel.starts_at < ends_at,
            SessionModel.ends_at > starts_at,
        )
        if exclude_session_id is not None:
            query = query.where(SessionModel.id != exclude_session_id)
        return await self._db.scalar(query) is not None

    async def update_session(self, session: Session) -> Session:
        model = await self._db.get(SessionModel, session.id)
        if model is None:
            return session
        model.movie_id = session.movie_id
        model.room_id = session.room_id
        model.starts_at = session.starts_at
        model.ends_at = session.ends_at
        model.price = session.price
        model.is_active = session.is_active
        await self._db.commit()
        await self._db.refresh(model)
        return self._to_domain(model)

    @staticmethod
    def _to_model(session: Session) -> SessionModel:
        return SessionModel(
            id=session.id,
            movie_id=session.movie_id,
            room_id=session.room_id,
            starts_at=session.starts_at,
            ends_at=session.ends_at,
            price=session.price,
            is_active=session.is_active,
        )

    @staticmethod
    def _to_domain(model: SessionModel) -> Session:
        return Session(
            id=model.id,
            movie_id=model.movie_id,
            room_id=model.room_id,
            starts_at=model.starts_at,
            ends_at=model.ends_at,
            price=model.price,
            is_active=model.is_active,
        )
