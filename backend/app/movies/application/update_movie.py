from uuid import UUID

from app.movies.domain.exceptions import MovieNotFoundError
from app.movies.domain.movie import Movie
from app.movies.domain.repository import MovieRepository


class UpdateMovie:
    def __init__(self, repository: MovieRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        movie_id: UUID,
        title: str | None = None,
        synopsis: str | None = None,
        age_rating: str | None = None,
        duration_minutes: int | None = None,
        genre: str | None = None,
        trailer_url: str | None = None,
    ) -> Movie:
        movie = await self._repository.find_movie_by_id(movie_id)
        if movie is None:
            raise MovieNotFoundError("Filme não encontrado.")

        if title is not None:
            movie.change_title(title)
        if synopsis is not None:
            movie.change_synopsis(synopsis)
        if age_rating is not None:
            movie.change_age_rating(age_rating)
        if duration_minutes is not None:
            movie.change_duration_minutes(duration_minutes)
        if genre is not None:
            movie.change_genre(genre)
        if trailer_url is not None:
            movie.change_trailer_url(trailer_url)

        return await self._repository.update_movie(movie)
