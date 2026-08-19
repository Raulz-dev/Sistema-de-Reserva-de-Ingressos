from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class MovieResponse(BaseModel):
    id: UUID
    title: str
    synopsis: str
    age_rating: str
    duration_minutes: int
    genre: str
    trailer_url: str | None


class CreateMovieRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    synopsis: str = Field(min_length=1)
    age_rating: str = Field(min_length=1, max_length=20)
    duration_minutes: int = Field(gt=0)
    genre: str = Field(min_length=1, max_length=100)
    trailer_url: HttpUrl | None = None


class UpdateMovieRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    synopsis: str | None = Field(default=None, min_length=1)
    age_rating: str | None = Field(default=None, min_length=1, max_length=20)
    duration_minutes: int | None = Field(default=None, gt=0)
    genre: str | None = Field(default=None, min_length=1, max_length=100)
    trailer_url: HttpUrl | None = None
