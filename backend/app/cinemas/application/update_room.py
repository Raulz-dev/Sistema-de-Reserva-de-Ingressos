from uuid import UUID

from app.cinemas.domain.exceptions import (
    CinemaNotFoundError,
    RoomNameAlreadyExistsError,
    RoomNotFoundError,
)
from app.cinemas.domain.repository import CinemaRepository, RoomRepository
from app.cinemas.domain.room import Room


class UpdateRoom:
    def __init__(
        self, cinema_repository: CinemaRepository, room_repository: RoomRepository
    ) -> None:
        self._cinema_repository = cinema_repository
        self._room_repository = room_repository

    async def execute(
        self,
        cinema_id: UUID,
        room_id: UUID,
        name: str | None = None,
        row_count: int | None = None,
        seats_per_row: int | None = None,
    ) -> Room:
        if await self._cinema_repository.find_cinema_by_id(cinema_id) is None:
            raise CinemaNotFoundError("Cinema não encontrado.")
        room = await self._room_repository.find_room_by_id(cinema_id, room_id)
        if room is None:
            raise RoomNotFoundError("Sala não encontrada.")

        if name is not None:
            previous_name = room.name
            room.change_name(name)
            if room.name != previous_name:
                existing = await self._room_repository.find_room_by_name(
                    cinema_id, room.name
                )
                if existing is not None:
                    raise RoomNameAlreadyExistsError("Já existe uma sala com este nome.")
        if row_count is not None:
            room.change_row_count(row_count)
        if seats_per_row is not None:
            room.change_seats_per_row(seats_per_row)

        return await self._room_repository.update_room(room)
