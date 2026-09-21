from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.cinemas.domain.repository import RoomRepository
from app.movies.domain.repository import MovieRepository
from app.sessions.domain.exceptions import (
    SessionConflictError,
    SessionMovieNotFoundError,
    SessionRoomNotFoundError,
)
from app.sessions.domain.repository import SessionRepository
from app.sessions.domain.session import Session


class CreateSession:
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
        movie_id: UUID,
        room_id: UUID,
        starts_at: datetime,
        ends_at: datetime,
        price: Decimal,
    ) -> Session:
        if await self._movie_repository.find_movie_by_id(movie_id) is None:
            raise SessionMovieNotFoundError("Filme ativo não encontrado.")
        if await self._room_repository.find_active_room_by_id(room_id) is None:
            raise SessionRoomNotFoundError("Sala ativa não encontrada.")

        session = Session(movie_id, room_id, starts_at, ends_at, price)
        if await self._repository.has_room_conflict(room_id, starts_at, ends_at):
            raise SessionConflictError("Já existe uma sessão nesse horário para a sala.")
        return await self._repository.create_session(session)
