from uuid import UUID

from app.movies.domain.exceptions import MovieNotFoundError
from app.movies.domain.movie import Movie
from app.movies.domain.repository import MovieRepository


class GetMovie:
    def __init__(self, repository: MovieRepository) -> None:
        self._repository = repository

    async def execute(self, movie_id: UUID) -> Movie:
        movie = await self._repository.find_movie_by_id(movie_id)
        if movie is None:
            raise MovieNotFoundError("Filme não encontrado.")
        return movie
