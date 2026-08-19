from app.movies.domain.movie import Movie
from app.movies.domain.repository import MovieRepository


class CreateMovie:
    def __init__(self, repository: MovieRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        title: str,
        synopsis: str,
        age_rating: str,
        duration_minutes: int,
        genre: str,
        trailer_url: str | None = None,
    ) -> Movie:
        movie = Movie(
            title=title,
            synopsis=synopsis,
            age_rating=age_rating,
            duration_minutes=duration_minutes,
            genre=genre,
            trailer_url=trailer_url,
        )
        return await self._repository.create_movie(movie)
