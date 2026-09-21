from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid7

import pytest

from app.cinemas.domain.room import Room
from app.movies.domain.movie import Movie
from app.sessions.application.create_session import CreateSession
from app.sessions.application.deactivate_session import DeactivateSession
from app.sessions.application.update_session import UpdateSession
from app.sessions.domain.exceptions import (
    InvalidSessionError,
    SessionConflictError,
    SessionMovieNotFoundError,
    SessionRoomNotFoundError,
)
from app.sessions.domain.session import Session
from app.sessions.presentation.schemas import CreateSessionRequest


class FakeSessionRepository:
    def __init__(self, sessions: list[Session] | None = None) -> None:
        self.sessions = sessions or []

    async def create_session(self, session):
        self.sessions.append(session)
        return session

    async def find_session_by_id(self, session_id):
        return next(
            (
                session
                for session in self.sessions
                if session.id == session_id and session.is_active
            ),
            None,
        )

    async def list_sessions(self):
        return [session for session in self.sessions if session.is_active]

    async def has_room_conflict(
        self, room_id, starts_at, ends_at, exclude_session_id=None
    ):
        return any(
            session.room_id == room_id
            and session.is_active
            and session.id != exclude_session_id
            and session.starts_at < ends_at
            and session.ends_at > starts_at
            for session in self.sessions
        )

    async def update_session(self, session):
        return session


class FakeMovieRepository:
    def __init__(self, movie: Movie | None) -> None:
        self.movie = movie

    async def find_movie_by_id(self, movie_id):
        if self.movie and self.movie.id == movie_id and self.movie.is_active:
            return self.movie
        return None


class FakeRoomRepository:
    def __init__(self, room: Room | None) -> None:
        self.room = room

    async def find_active_room_by_id(self, room_id):
        if self.room and self.room.id == room_id and self.room.is_active:
            return self.room
        return None


def make_movie() -> Movie:
    return Movie("Filme", "Sinopse", "12", 120, "Drama")


def make_room() -> Room:
    return Room(uuid7(), "Sala 1", 10, 10)


def make_period(hour: int = 14) -> tuple[datetime, datetime]:
    starts_at = datetime(2026, 10, 1, hour, tzinfo=UTC)
    return starts_at, starts_at + timedelta(hours=2)


def make_session(movie: Movie, room: Room, hour: int = 14) -> Session:
    starts_at, ends_at = make_period(hour)
    return Session(movie.id, room.id, starts_at, ends_at, Decimal("25.00"))


def test_session_rejects_invalid_period() -> None:
    starts_at, _ = make_period()
    with pytest.raises(InvalidSessionError, match="posterior"):
        Session(uuid7(), uuid7(), starts_at, starts_at, Decimal("25.00"))


def test_session_rejects_datetime_without_timezone() -> None:
    starts_at = datetime(2026, 10, 1, 14)  # noqa: DTZ001 - cenário inválido intencional
    ends_at = starts_at + timedelta(hours=2)

    with pytest.raises(InvalidSessionError, match="fuso horário"):
        Session(uuid7(), uuid7(), starts_at, ends_at, Decimal("25.00"))


def test_create_schema_rejects_datetime_without_timezone() -> None:
    with pytest.raises(ValueError, match="timezone"):
        CreateSessionRequest(
            movie_id=uuid7(),
            room_id=uuid7(),
            starts_at="2026-10-01T14:00:00",
            ends_at="2026-10-01T16:00:00",
            price=Decimal("25.00"),
        )


def test_session_rejects_non_positive_price() -> None:
    starts_at, ends_at = make_period()
    with pytest.raises(InvalidSessionError, match="preço"):
        Session(uuid7(), uuid7(), starts_at, ends_at, Decimal(0))


@pytest.mark.asyncio
async def test_create_session_with_active_movie_and_room() -> None:
    movie = make_movie()
    room = make_room()
    starts_at, ends_at = make_period()

    session = await CreateSession(
        FakeSessionRepository(), FakeMovieRepository(movie), FakeRoomRepository(room)
    ).execute(movie.id, room.id, starts_at, ends_at, Decimal("25.00"))

    assert session.movie_id == movie.id
    assert session.room_id == room.id


@pytest.mark.asyncio
async def test_create_session_rejects_inactive_movie() -> None:
    movie = make_movie()
    movie.deactivate()
    room = make_room()
    starts_at, ends_at = make_period()

    with pytest.raises(SessionMovieNotFoundError):
        await CreateSession(
            FakeSessionRepository(), FakeMovieRepository(movie), FakeRoomRepository(room)
        ).execute(movie.id, room.id, starts_at, ends_at, Decimal("25.00"))


@pytest.mark.asyncio
async def test_create_session_rejects_inactive_room() -> None:
    movie = make_movie()
    room = make_room()
    room.deactivate()
    starts_at, ends_at = make_period()

    with pytest.raises(SessionRoomNotFoundError):
        await CreateSession(
            FakeSessionRepository(), FakeMovieRepository(movie), FakeRoomRepository(room)
        ).execute(movie.id, room.id, starts_at, ends_at, Decimal("25.00"))


@pytest.mark.asyncio
async def test_create_session_rejects_room_schedule_conflict() -> None:
    movie = make_movie()
    room = make_room()
    existing = make_session(movie, room)
    starts_at = existing.starts_at + timedelta(minutes=30)
    ends_at = existing.ends_at + timedelta(minutes=30)

    with pytest.raises(SessionConflictError):
        await CreateSession(
            FakeSessionRepository([existing]),
            FakeMovieRepository(movie),
            FakeRoomRepository(room),
        ).execute(movie.id, room.id, starts_at, ends_at, Decimal("25.00"))


@pytest.mark.asyncio
async def test_create_session_allows_adjacent_period() -> None:
    movie = make_movie()
    room = make_room()
    existing = make_session(movie, room)
    starts_at = existing.ends_at
    ends_at = starts_at + timedelta(hours=2)

    created = await CreateSession(
        FakeSessionRepository([existing]),
        FakeMovieRepository(movie),
        FakeRoomRepository(room),
    ).execute(movie.id, room.id, starts_at, ends_at, Decimal("25.00"))

    assert created.starts_at == existing.ends_at


@pytest.mark.asyncio
async def test_update_session_rejects_conflicting_period() -> None:
    movie = make_movie()
    room = make_room()
    first = make_session(movie, room, 14)
    second = make_session(movie, room, 18)

    with pytest.raises(SessionConflictError):
        await UpdateSession(
            FakeSessionRepository([first, second]),
            FakeMovieRepository(movie),
            FakeRoomRepository(room),
        ).execute(second.id, starts_at=first.starts_at + timedelta(minutes=30))


@pytest.mark.asyncio
async def test_deactivate_session_hides_it_from_active_lookup() -> None:
    movie = make_movie()
    room = make_room()
    session = make_session(movie, room)
    repository = FakeSessionRepository([session])

    await DeactivateSession(repository).execute(session.id)

    assert await repository.find_session_by_id(session.id) is None
