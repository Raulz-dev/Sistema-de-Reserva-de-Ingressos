from app.movies.domain.movie import Movie
from app.movies.domain.repository import MovieRepository


class ListMovies:
    def __init__(self, repository: MovieRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[Movie]:
        return await self._repository.list_movies()
