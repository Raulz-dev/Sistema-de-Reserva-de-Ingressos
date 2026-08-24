from app.cinemas.domain.cinema import Cinema
from app.cinemas.domain.repository import CinemaRepository


class ListCinemas:
    def __init__(self, repository: CinemaRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[Cinema]:
        return await self._repository.list_cinemas()
