from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cinemas.application.create_cinema import CreateCinema
from app.cinemas.application.create_room import CreateRoom
from app.cinemas.application.deactivate_cinema import DeactivateCinema
from app.cinemas.application.deactivate_room import DeactivateRoom
from app.cinemas.application.get_cinema import GetCinema
from app.cinemas.application.get_room import GetRoom
from app.cinemas.application.list_cinemas import ListCinemas
from app.cinemas.application.list_rooms import ListRooms
from app.cinemas.application.update_cinema import UpdateCinema
from app.cinemas.application.update_room import UpdateRoom
from app.cinemas.infrastructure.repository import (
    SQLAlchemyCinemaRepository,
    SQLAlchemyRoomRepository,
)
from app.database.session import get_db


def get_cinema_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SQLAlchemyCinemaRepository:
    return SQLAlchemyCinemaRepository(db)


def get_room_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SQLAlchemyRoomRepository:
    return SQLAlchemyRoomRepository(db)


def get_create_cinema(
    repository: Annotated[SQLAlchemyCinemaRepository, Depends(get_cinema_repository)],
) -> CreateCinema:
    return CreateCinema(repository)


def get_list_cinemas(
    repository: Annotated[SQLAlchemyCinemaRepository, Depends(get_cinema_repository)],
) -> ListCinemas:
    return ListCinemas(repository)


def get_cinema(
    repository: Annotated[SQLAlchemyCinemaRepository, Depends(get_cinema_repository)],
) -> GetCinema:
    return GetCinema(repository)


def get_update_cinema(
    repository: Annotated[SQLAlchemyCinemaRepository, Depends(get_cinema_repository)],
) -> UpdateCinema:
    return UpdateCinema(repository)


def get_deactivate_cinema(
    repository: Annotated[SQLAlchemyCinemaRepository, Depends(get_cinema_repository)],
) -> DeactivateCinema:
    return DeactivateCinema(repository)


def get_create_room(
    cinema_repository: Annotated[
        SQLAlchemyCinemaRepository, Depends(get_cinema_repository)
    ],
    room_repository: Annotated[SQLAlchemyRoomRepository, Depends(get_room_repository)],
) -> CreateRoom:
    return CreateRoom(cinema_repository, room_repository)


def get_list_rooms(
    cinema_repository: Annotated[
        SQLAlchemyCinemaRepository, Depends(get_cinema_repository)
    ],
    room_repository: Annotated[SQLAlchemyRoomRepository, Depends(get_room_repository)],
) -> ListRooms:
    return ListRooms(cinema_repository, room_repository)


def get_room(
    cinema_repository: Annotated[
        SQLAlchemyCinemaRepository, Depends(get_cinema_repository)
    ],
    room_repository: Annotated[SQLAlchemyRoomRepository, Depends(get_room_repository)],
) -> GetRoom:
    return GetRoom(cinema_repository, room_repository)


def get_update_room(
    cinema_repository: Annotated[
        SQLAlchemyCinemaRepository, Depends(get_cinema_repository)
    ],
    room_repository: Annotated[SQLAlchemyRoomRepository, Depends(get_room_repository)],
) -> UpdateRoom:
    return UpdateRoom(cinema_repository, room_repository)


def get_deactivate_room(
    cinema_repository: Annotated[
        SQLAlchemyCinemaRepository, Depends(get_cinema_repository)
    ],
    room_repository: Annotated[SQLAlchemyRoomRepository, Depends(get_room_repository)],
) -> DeactivateRoom:
    return DeactivateRoom(cinema_repository, room_repository)
