from uuid import UUID

from app.cinemas.domain.exceptions import CinemaNotFoundError
from app.cinemas.domain.repository import CinemaRepository, RoomRepository
from app.cinemas.domain.room import Room


class ListRooms:
    def __init__(
        self, cinema_repository: CinemaRepository, room_repository: RoomRepository
    ) -> None:
        self._cinema_repository = cinema_repository
        self._room_repository = room_repository

    async def execute(self, cinema_id: UUID) -> list[Room]:
        if await self._cinema_repository.find_cinema_by_id(cinema_id) is None:
            raise CinemaNotFoundError("Cinema não encontrado.")
        return await self._room_repository.list_rooms(cinema_id)
