from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.movies.domain.movie import Movie
from app.movies.domain.repository import MovieRepository
from app.movies.infrastructure.model import MovieModel


class SQLAlchemyMovieRepository(MovieRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_movie(self, movie: Movie) -> Movie:
        model = self._to_model(movie)
        self._db.add(model)
        await self._db.commit()
        await self._db.refresh(model)
        return self._to_domain(model)

    async def find_movie_by_id(self, movie_id: UUID) -> Movie | None:
        model = await self._db.get(MovieModel, movie_id)
        return None if model is None else self._to_domain(model)

    async def list_movies(self) -> list[Movie]:
        result = await self._db.scalars(select(MovieModel).order_by(MovieModel.title))
        return [self._to_domain(model) for model in result.all()]

    async def update_movie(self, movie: Movie) -> Movie:
        model = await self._db.get(MovieModel, movie.id)
        if model is None:
            return movie

        model.title = movie.title
        model.synopsis = movie.synopsis
        model.age_rating = movie.age_rating
        model.duration_minutes = movie.duration_minutes
        model.genre = movie.genre
        model.trailer_url = movie.trailer_url
        await self._db.commit()
        await self._db.refresh(model)
        return self._to_domain(model)

    async def delete_movie(self, movie_id: UUID) -> None:
        await self._db.execute(delete(MovieModel).where(MovieModel.id == movie_id))
        await self._db.commit()

    @staticmethod
    def _to_model(movie: Movie) -> MovieModel:
        return MovieModel(
            id=movie.id,
            title=movie.title,
            synopsis=movie.synopsis,
            age_rating=movie.age_rating,
            duration_minutes=movie.duration_minutes,
            genre=movie.genre,
            trailer_url=movie.trailer_url,
        )

    @staticmethod
    def _to_domain(model: MovieModel) -> Movie:
        return Movie(
            id=model.id,
            title=model.title,
            synopsis=model.synopsis,
            age_rating=model.age_rating,
            duration_minutes=model.duration_minutes,
            genre=model.genre,
            trailer_url=model.trailer_url,
        )
