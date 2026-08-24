from uuid import UUID

from pydantic import BaseModel, Field


class CinemaResponse(BaseModel):
    id: UUID
    name: str
    street: str
    number: str
    complement: str | None
    neighborhood: str
    zip_code: str
    is_active: bool


class CreateCinemaRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    street: str = Field(min_length=1, max_length=200)
    number: str = Field(min_length=1, max_length=30)
    complement: str | None = Field(default=None, max_length=100)
    neighborhood: str = Field(min_length=1, max_length=100)
    zip_code: str = Field(min_length=8, max_length=9)


class UpdateCinemaRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    street: str | None = Field(default=None, min_length=1, max_length=200)
    number: str | None = Field(default=None, min_length=1, max_length=30)
    complement: str | None = Field(default=None, max_length=100)
    neighborhood: str | None = Field(default=None, min_length=1, max_length=100)
    zip_code: str | None = Field(default=None, min_length=8, max_length=9)


class RoomResponse(BaseModel):
    id: UUID
    cinema_id: UUID
    name: str
    row_count: int
    seats_per_row: int
    capacity: int
    is_active: bool


class CreateRoomRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    row_count: int = Field(gt=0)
    seats_per_row: int = Field(gt=0)


class UpdateRoomRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    row_count: int | None = Field(default=None, gt=0)
    seats_per_row: int | None = Field(default=None, gt=0)
