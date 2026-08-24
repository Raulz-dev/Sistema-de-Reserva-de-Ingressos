from uuid import UUID

from app.cinemas.domain.exceptions import (
    CinemaNotFoundError,
    RoomNameAlreadyExistsError,
)
from app.cinemas.domain.repository import CinemaRepository, RoomRepository
from app.cinemas.domain.room import Room


class CreateRoom:
    def __init__(
        self, cinema_repository: CinemaRepository, room_repository: RoomRepository
    ) -> None:
        self._cinema_repository = cinema_repository
        self._room_repository = room_repository

    async def execute(
        self, cinema_id: UUID, name: str, row_count: int, seats_per_row: int
    ) -> Room:
        if await self._cinema_repository.find_cinema_by_id(cinema_id) is None:
            raise CinemaNotFoundError("Cinema não encontrado.")
        room = Room(
            cinema_id=cinema_id,
            name=name,
            row_count=row_count,
            seats_per_row=seats_per_row,
        )
        if await self._room_repository.find_room_by_name(cinema_id, room.name) is not None:
            raise RoomNameAlreadyExistsError("Já existe uma sala com este nome.")
        return await self._room_repository.create_room(room)
