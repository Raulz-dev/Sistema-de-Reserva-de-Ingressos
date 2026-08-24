from uuid import UUID

from app.cinemas.domain.cinema import Cinema
from app.cinemas.domain.exceptions import (
    CinemaNameAlreadyExistsError,
    CinemaNotFoundError,
)
from app.cinemas.domain.repository import CinemaRepository


class UpdateCinema:
    def __init__(self, repository: CinemaRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        cinema_id: UUID,
        name: str | None = None,
        street: str | None = None,
        number: str | None = None,
        complement: str | None = None,
        neighborhood: str | None = None,
        zip_code: str | None = None,
    ) -> Cinema:
        cinema = await self._repository.find_cinema_by_id(cinema_id)
        if cinema is None:
            raise CinemaNotFoundError("Cinema não encontrado.")

        if name is not None:
            previous_name = cinema.name
            cinema.change_name(name)
            if (
                cinema.name != previous_name
                and await self._repository.find_cinema_by_name(cinema.name) is not None
            ):
                raise CinemaNameAlreadyExistsError("Já existe um cinema com este nome.")
        if street is not None:
            cinema.change_street(street)
        if number is not None:
            cinema.change_number(number)
        if complement is not None:
            cinema.change_complement(complement)
        if neighborhood is not None:
            cinema.change_neighborhood(neighborhood)
        if zip_code is not None:
            cinema.change_zip_code(zip_code)

        return await self._repository.update_cinema(cinema)
