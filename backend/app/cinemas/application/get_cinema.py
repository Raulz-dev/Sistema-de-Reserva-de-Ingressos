from uuid import UUID

from app.cinemas.domain.cinema import Cinema
from app.cinemas.domain.exceptions import CinemaNotFoundError
from app.cinemas.domain.repository import CinemaRepository


class GetCinema:
    def __init__(self, repository: CinemaRepository) -> None:
        self._repository = repository

    async def execute(self, cinema_id: UUID) -> Cinema:
        cinema = await self._repository.find_cinema_by_id(cinema_id)
        if cinema is None:
            raise CinemaNotFoundError("Cinema não encontrado.")
        return cinema
