from uuid import UUID

from app.movies.domain.exceptions import MovieNotFoundError
from app.movies.domain.repository import MovieRepository


class DeleteMovie:
    def __init__(self, repository: MovieRepository) -> None:
        self._repository = repository

    async def execute(self, movie_id: UUID) -> None:
        if await self._repository.find_movie_by_id(movie_id) is None:
            raise MovieNotFoundError("Filme não encontrado.")
        await self._repository.delete_movie(movie_id)
