from uuid import UUID

from app.movies.domain.exceptions import MovieNotFoundError
from app.movies.domain.repository import MovieRepository


class DeleteMovie:
    def __init__(self, repository: MovieRepository) -> None:
        self._repository = repository

    async def execute(self, movie_id: UUID) -> None:
        movie = await self._repository.find_movie_by_id(movie_id)
        if movie is None:
            raise MovieNotFoundError("Filme não encontrado.")
        movie.deactivate()
        await self._repository.update_movie(movie)
