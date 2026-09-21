from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cinemas.infrastructure.repository import SQLAlchemyRoomRepository
from app.database.session import get_db
from app.movies.infrastructure.repository import SQLAlchemyMovieRepository
from app.sessions.application.create_session import CreateSession
from app.sessions.application.deactivate_session import DeactivateSession
from app.sessions.application.get_session import GetSession
from app.sessions.application.list_sessions import ListSessions
from app.sessions.application.update_session import UpdateSession
from app.sessions.infrastructure.repository import SQLAlchemySessionRepository


def get_session_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SQLAlchemySessionRepository:
    return SQLAlchemySessionRepository(db)


def get_movie_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SQLAlchemyMovieRepository:
    return SQLAlchemyMovieRepository(db)


def get_room_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SQLAlchemyRoomRepository:
    return SQLAlchemyRoomRepository(db)


def get_create_session(
    repository: Annotated[SQLAlchemySessionRepository, Depends(get_session_repository)],
    movie_repository: Annotated[
        SQLAlchemyMovieRepository, Depends(get_movie_repository)
    ],
    room_repository: Annotated[SQLAlchemyRoomRepository, Depends(get_room_repository)],
) -> CreateSession:
    return CreateSession(repository, movie_repository, room_repository)


def get_list_sessions(
    repository: Annotated[SQLAlchemySessionRepository, Depends(get_session_repository)],
) -> ListSessions:
    return ListSessions(repository)


def get_session(
    repository: Annotated[SQLAlchemySessionRepository, Depends(get_session_repository)],
) -> GetSession:
    return GetSession(repository)


def get_update_session(
    repository: Annotated[SQLAlchemySessionRepository, Depends(get_session_repository)],
    movie_repository: Annotated[
        SQLAlchemyMovieRepository, Depends(get_movie_repository)
    ],
    room_repository: Annotated[SQLAlchemyRoomRepository, Depends(get_room_repository)],
) -> UpdateSession:
    return UpdateSession(repository, movie_repository, room_repository)


def get_deactivate_session(
    repository: Annotated[SQLAlchemySessionRepository, Depends(get_session_repository)],
) -> DeactivateSession:
    return DeactivateSession(repository)
