from app.cinemas.domain.cinema import Cinema
from app.cinemas.domain.exceptions import CinemaNameAlreadyExistsError
from app.cinemas.domain.repository import CinemaRepository


class CreateCinema:
    def __init__(self, repository: CinemaRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        name: str,
        street: str,
        number: str,
        neighborhood: str,
        zip_code: str,
        complement: str | None = None,
    ) -> Cinema:
        cinema = Cinema(
            name=name,
            street=street,
            number=number,
            complement=complement,
            neighborhood=neighborhood,
            zip_code=zip_code,
        )
        if await self._repository.find_cinema_by_name(cinema.name) is not None:
            raise CinemaNameAlreadyExistsError("Já existe um cinema com este nome.")
        return await self._repository.create_cinema(cinema)
