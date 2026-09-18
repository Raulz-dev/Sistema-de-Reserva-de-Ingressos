from uuid import uuid7

import pytest

from app.movies.application.delete_movie import DeleteMovie
from app.movies.application.update_movie import UpdateMovie
from app.movies.domain.exceptions import InvalidMovieError, MovieNotFoundError
from app.movies.domain.movie import Movie
from app.movies.presentation.schemas import UpdateMovieRequest


class FakeMovieRepository:
    def __init__(self, movie: Movie | None = None) -> None:
        self.movie = movie

    async def find_movie_by_id(self, movie_id):
        if self.movie is None or self.movie.id != movie_id or not self.movie.is_active:
            return None
        return self.movie

    async def update_movie(self, movie):
        self.movie = movie
        return movie


def make_movie(trailer_url: str | None = "https://example.com/trailer") -> Movie:
    return Movie(
        title="Filme Teste",
        synopsis="Sinopse do filme",
        age_rating="12",
        duration_minutes=120,
        genre="Drama",
        trailer_url=trailer_url,
    )


def test_movie_rejects_non_positive_duration() -> None:
    with pytest.raises(InvalidMovieError, match="duração"):
        Movie("Filme", "Sinopse", "Livre", 0, "Drama")


def test_update_schema_distinguishes_omitted_and_explicit_null_trailer() -> None:
    omitted = UpdateMovieRequest()
    explicit_null = UpdateMovieRequest(trailer_url=None)

    assert "trailer_url" not in omitted.model_fields_set
    assert "trailer_url" in explicit_null.model_fields_set


@pytest.mark.asyncio
async def test_update_movie_clears_trailer_when_explicitly_requested() -> None:
    movie = make_movie()
    repository = FakeMovieRepository(movie)

    updated = await UpdateMovie(repository).execute(
        movie.id, trailer_url=None, trailer_url_set=True
    )

    assert updated.trailer_url is None


@pytest.mark.asyncio
async def test_delete_movie_deactivates_instead_of_removing() -> None:
    movie = make_movie()
    repository = FakeMovieRepository(movie)

    await DeleteMovie(repository).execute(movie.id)

    assert repository.movie is not None
    assert repository.movie.is_active is False


@pytest.mark.asyncio
async def test_delete_movie_rejects_nonexistent_movie() -> None:
    with pytest.raises(MovieNotFoundError, match="Filme não encontrado"):
        await DeleteMovie(FakeMovieRepository()).execute(uuid7())
