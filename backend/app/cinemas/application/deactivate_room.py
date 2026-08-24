from uuid import UUID

from app.cinemas.domain.exceptions import CinemaNotFoundError, RoomNotFoundError
from app.cinemas.domain.repository import CinemaRepository, RoomRepository


class DeactivateRoom:
    def __init__(
        self, cinema_repository: CinemaRepository, room_repository: RoomRepository
    ) -> None:
        self._cinema_repository = cinema_repository
        self._room_repository = room_repository

    async def execute(self, cinema_id: UUID, room_id: UUID) -> None:
        if await self._cinema_repository.find_cinema_by_id(cinema_id) is None:
            raise CinemaNotFoundError("Cinema não encontrado.")
        room = await self._room_repository.find_room_by_id(cinema_id, room_id)
        if room is None:
            raise RoomNotFoundError("Sala não encontrada.")
        room.deactivate()
        await self._room_repository.update_room(room)
