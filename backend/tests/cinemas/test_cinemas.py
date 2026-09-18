from uuid import uuid7

import pytest

from app.cinemas.application.update_cinema import UpdateCinema
from app.cinemas.domain.cinema import Cinema
from app.cinemas.domain.exceptions import InvalidCinemaError, InvalidRoomError
from app.cinemas.domain.room import Room
from app.cinemas.presentation.schemas import UpdateCinemaRequest


class FakeCinemaRepository:
    def __init__(self, cinema: Cinema) -> None:
        self.cinema = cinema

    async def find_cinema_by_id(self, cinema_id):
        return self.cinema if self.cinema.id == cinema_id else None

    async def find_cinema_by_name(self, name):
        return self.cinema if self.cinema.name == name else None

    async def update_cinema(self, cinema):
        self.cinema = cinema
        return cinema


def make_cinema(complement: str | None = "Shopping") -> Cinema:
    return Cinema(
        name="Cinema Teste",
        street="Rua Principal",
        number="100",
        neighborhood="Centro",
        zip_code="60000-000",
        complement=complement,
    )


def test_cinema_normalizes_zip_code() -> None:
    assert make_cinema().zip_code == "60000000"


def test_cinema_rejects_invalid_zip_code() -> None:
    with pytest.raises(InvalidCinemaError, match="CEP"):
        Cinema("Cinema", "Rua", "1", "Centro", "123")


def test_room_calculates_capacity() -> None:
    room = Room(uuid7(), "Sala 1", row_count=10, seats_per_row=12)

    assert room.capacity == 120


def test_room_rejects_invalid_dimensions() -> None:
    with pytest.raises(InvalidRoomError, match="inteiro positivo"):
        Room(uuid7(), "Sala 1", row_count=0, seats_per_row=12)


def test_update_schema_distinguishes_omitted_and_explicit_null_complement() -> None:
    omitted = UpdateCinemaRequest()
    explicit_null = UpdateCinemaRequest(complement=None)

    assert "complement" not in omitted.model_fields_set
    assert "complement" in explicit_null.model_fields_set


@pytest.mark.asyncio
async def test_update_cinema_clears_complement_when_explicitly_requested() -> None:
    cinema = make_cinema()
    repository = FakeCinemaRepository(cinema)

    updated = await UpdateCinema(repository).execute(
        cinema.id, complement=None, complement_set=True
    )

    assert updated.complement is None
