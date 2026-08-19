from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.movies.application.create_movie import CreateMovie
from app.movies.application.delete_movie import DeleteMovie
from app.movies.application.get_movie import GetMovie
from app.movies.application.list_movies import ListMovies
from app.movies.application.update_movie import UpdateMovie
from app.movies.domain.exceptions import MovieNotFoundError
from app.movies.domain.movie import Movie
from app.movies.presentation.dependencies import (
    get_create_movie,
    get_delete_movie,
    get_list_movies,
    get_movie,
    get_update_movie,
)
from app.movies.presentation.schemas import (
    CreateMovieRequest,
    MovieResponse,
    UpdateMovieRequest,
)
from app.users.domain.user import User
from app.users.presentation.dependencies import require_admin

router = APIRouter(prefix="/movies", tags=["Movies"])


def to_response(movie: Movie) -> MovieResponse:
    return MovieResponse(
        id=movie.id,
        title=movie.title,
        synopsis=movie.synopsis,
        age_rating=movie.age_rating,
        duration_minutes=movie.duration_minutes,
        genre=movie.genre,
        trailer_url=movie.trailer_url,
    )


@router.post("", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
async def create_movie(
    data: CreateMovieRequest,
    use_case: Annotated[CreateMovie, Depends(get_create_movie)],
    _: Annotated[User, Depends(require_admin)],
) -> MovieResponse:
    movie = await use_case.execute(
        title=data.title,
        synopsis=data.synopsis,
        age_rating=data.age_rating,
        duration_minutes=data.duration_minutes,
        genre=data.genre,
        trailer_url=str(data.trailer_url) if data.trailer_url else None,
    )
    return to_response(movie)


@router.get("", response_model=list[MovieResponse])
async def list_movies(
    use_case: Annotated[ListMovies, Depends(get_list_movies)],
) -> list[MovieResponse]:
    return [to_response(movie) for movie in await use_case.execute()]


@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie_by_id(
    movie_id: UUID,
    use_case: Annotated[GetMovie, Depends(get_movie)],
) -> MovieResponse:
    try:
        return to_response(await use_case.execute(movie_id))
    except MovieNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
        ) from error


@router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie(
    movie_id: UUID,
    data: UpdateMovieRequest,
    use_case: Annotated[UpdateMovie, Depends(get_update_movie)],
    _: Annotated[User, Depends(require_admin)],
) -> MovieResponse:
    try:
        movie = await use_case.execute(
            movie_id=movie_id,
            title=data.title,
            synopsis=data.synopsis,
            age_rating=data.age_rating,
            duration_minutes=data.duration_minutes,
            genre=data.genre,
            trailer_url=str(data.trailer_url) if data.trailer_url else None,
        )
        return to_response(movie)
    except MovieNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
        ) from error


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(
    movie_id: UUID,
    use_case: Annotated[DeleteMovie, Depends(get_delete_movie)],
    _: Annotated[User, Depends(require_admin)],
) -> Response:
    try:
        await use_case.execute(movie_id)
    except MovieNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
        ) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
