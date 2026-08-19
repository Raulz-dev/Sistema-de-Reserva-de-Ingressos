from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.movies.application.create_movie import CreateMovie
from app.movies.application.delete_movie import DeleteMovie
from app.movies.application.get_movie import GetMovie
from app.movies.application.list_movies import ListMovies
from app.movies.application.update_movie import UpdateMovie
from app.movies.infrastructure.repository import SQLAlchemyMovieRepository


def get_movie_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SQLAlchemyMovieRepository:
    return SQLAlchemyMovieRepository(db)


def get_create_movie(
    repository: Annotated[SQLAlchemyMovieRepository, Depends(get_movie_repository)],
) -> CreateMovie:
    return CreateMovie(repository)


def get_list_movies(
    repository: Annotated[SQLAlchemyMovieRepository, Depends(get_movie_repository)],
) -> ListMovies:
    return ListMovies(repository)


def get_movie(
    repository: Annotated[SQLAlchemyMovieRepository, Depends(get_movie_repository)],
) -> GetMovie:
    return GetMovie(repository)


def get_update_movie(
    repository: Annotated[SQLAlchemyMovieRepository, Depends(get_movie_repository)],
) -> UpdateMovie:
    return UpdateMovie(repository)


def get_delete_movie(
    repository: Annotated[SQLAlchemyMovieRepository, Depends(get_movie_repository)],
) -> DeleteMovie:
    return DeleteMovie(repository)
