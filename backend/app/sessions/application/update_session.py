from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.cinemas.domain.repository import RoomRepository
from app.movies.domain.repository import MovieRepository
from app.sessions.domain.exceptions import (
    SessionConflictError,
    SessionMovieNotFoundError,
    SessionNotFoundError,
    SessionRoomNotFoundError,
)
from app.sessions.domain.repository import SessionRepository
from app.sessions.domain.session import Session


class UpdateSession:
    def __init__(
        self,
        repository: SessionRepository,
        movie_repository: MovieRepository,
        room_repository: RoomRepository,
    ) -> None:
        self._repository = repository
        self._movie_repository = movie_repository
        self._room_repository = room_repository

    async def execute(
        self,
        session_id: UUID,
        movie_id: UUID | None = None,
        room_id: UUID | None = None,
        starts_at: datetime | None = None,
        ends_at: datetime | None = None,
        price: Decimal | None = None,
    ) -> Session:
        session = await self._repository.find_session_by_id(session_id)
        if session is None:
            raise SessionNotFoundError("Sessão não encontrada.")

        if movie_id is not None:
            if await self._movie_repository.find_movie_by_id(movie_id) is None:
                raise SessionMovieNotFoundError("Filme ativo não encontrado.")
            session.change_movie(movie_id)
        if room_id is not None:
            if await self._room_repository.find_active_room_by_id(room_id) is None:
                raise SessionRoomNotFoundError("Sala ativa não encontrada.")
            session.change_room(room_id)

        new_starts_at = starts_at or session.starts_at
        new_ends_at = ends_at or session.ends_at
        session.change_period(new_starts_at, new_ends_at)

        if await self._repository.has_room_conflict(
            session.room_id,
            session.starts_at,
            session.ends_at,
            exclude_session_id=session.id,
        ):
            raise SessionConflictError("Já existe uma sessão nesse horário para a sala.")
        if price is not None:
            session.change_price(price)
        return await self._repository.update_session(session)
