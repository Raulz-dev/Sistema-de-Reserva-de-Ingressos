from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.cinemas.application.create_cinema import CreateCinema
from app.cinemas.application.create_room import CreateRoom
from app.cinemas.application.deactivate_cinema import DeactivateCinema
from app.cinemas.application.deactivate_room import DeactivateRoom
from app.cinemas.application.get_cinema import GetCinema
from app.cinemas.application.get_room import GetRoom
from app.cinemas.application.list_cinemas import ListCinemas
from app.cinemas.application.list_rooms import ListRooms
from app.cinemas.application.update_cinema import UpdateCinema
from app.cinemas.application.update_room import UpdateRoom
from app.cinemas.domain.cinema import Cinema
from app.cinemas.domain.exceptions import (
    CinemaNameAlreadyExistsError,
    CinemaNotFoundError,
    RoomNameAlreadyExistsError,
    RoomNotFoundError,
)
from app.cinemas.domain.room import Room
from app.cinemas.presentation.dependencies import (
    get_cinema,
    get_create_cinema,
    get_create_room,
    get_deactivate_cinema,
    get_deactivate_room,
    get_list_cinemas,
    get_list_rooms,
    get_room,
    get_update_cinema,
    get_update_room,
)
from app.cinemas.presentation.schemas import (
    CinemaResponse,
    CreateCinemaRequest,
    CreateRoomRequest,
    RoomResponse,
    UpdateCinemaRequest,
    UpdateRoomRequest,
)
from app.users.domain.user import User
from app.users.presentation.dependencies import require_admin

router = APIRouter(prefix="/cinemas", tags=["Cinemas"])


def cinema_to_response(cinema: Cinema) -> CinemaResponse:
    return CinemaResponse(
        id=cinema.id,
        name=cinema.name,
        street=cinema.street,
        number=cinema.number,
        complement=cinema.complement,
        neighborhood=cinema.neighborhood,
        zip_code=cinema.zip_code,
        is_active=cinema.is_active,
    )


def room_to_response(room: Room) -> RoomResponse:
    return RoomResponse(
        id=room.id,
        cinema_id=room.cinema_id,
        name=room.name,
        row_count=room.row_count,
        seats_per_row=room.seats_per_row,
        capacity=room.capacity,
        is_active=room.is_active,
    )


@router.post("", response_model=CinemaResponse, status_code=status.HTTP_201_CREATED)
async def create_cinema(
    data: CreateCinemaRequest,
    use_case: Annotated[CreateCinema, Depends(get_create_cinema)],
    _: Annotated[User, Depends(require_admin)],
) -> CinemaResponse:
    try:
        cinema = await use_case.execute(**data.model_dump())
        return cinema_to_response(cinema)
    except CinemaNameAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.get("", response_model=list[CinemaResponse])
async def list_cinemas(
    use_case: Annotated[ListCinemas, Depends(get_list_cinemas)],
) -> list[CinemaResponse]:
    return [cinema_to_response(cinema) for cinema in await use_case.execute()]


@router.get("/{cinema_id}", response_model=CinemaResponse)
async def get_cinema_by_id(
    cinema_id: UUID,
    use_case: Annotated[GetCinema, Depends(get_cinema)],
) -> CinemaResponse:
    try:
        return cinema_to_response(await use_case.execute(cinema_id))
    except CinemaNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.put("/{cinema_id}", response_model=CinemaResponse)
async def update_cinema(
    cinema_id: UUID,
    data: UpdateCinemaRequest,
    use_case: Annotated[UpdateCinema, Depends(get_update_cinema)],
    _: Annotated[User, Depends(require_admin)],
) -> CinemaResponse:
    try:
        cinema = await use_case.execute(cinema_id, **data.model_dump())
        return cinema_to_response(cinema)
    except CinemaNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except CinemaNameAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.delete("/{cinema_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_cinema(
    cinema_id: UUID,
    use_case: Annotated[DeactivateCinema, Depends(get_deactivate_cinema)],
    _: Annotated[User, Depends(require_admin)],
) -> Response:
    try:
        await use_case.execute(cinema_id)
    except CinemaNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{cinema_id}/rooms", response_model=RoomResponse, status_code=status.HTTP_201_CREATED
)
async def create_room(
    cinema_id: UUID,
    data: CreateRoomRequest,
    use_case: Annotated[CreateRoom, Depends(get_create_room)],
    _: Annotated[User, Depends(require_admin)],
) -> RoomResponse:
    try:
        room = await use_case.execute(cinema_id, **data.model_dump())
        return room_to_response(room)
    except CinemaNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except RoomNameAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.get("/{cinema_id}/rooms", response_model=list[RoomResponse])
async def list_rooms(
    cinema_id: UUID,
    use_case: Annotated[ListRooms, Depends(get_list_rooms)],
) -> list[RoomResponse]:
    try:
        return [room_to_response(room) for room in await use_case.execute(cinema_id)]
    except CinemaNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.get("/{cinema_id}/rooms/{room_id}", response_model=RoomResponse)
async def get_room_by_id(
    cinema_id: UUID,
    room_id: UUID,
    use_case: Annotated[GetRoom, Depends(get_room)],
) -> RoomResponse:
    try:
        return room_to_response(await use_case.execute(cinema_id, room_id))
    except (CinemaNotFoundError, RoomNotFoundError) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.put("/{cinema_id}/rooms/{room_id}", response_model=RoomResponse)
async def update_room(
    cinema_id: UUID,
    room_id: UUID,
    data: UpdateRoomRequest,
    use_case: Annotated[UpdateRoom, Depends(get_update_room)],
    _: Annotated[User, Depends(require_admin)],
) -> RoomResponse:
    try:
        room = await use_case.execute(cinema_id, room_id, **data.model_dump())
        return room_to_response(room)
    except (CinemaNotFoundError, RoomNotFoundError) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except RoomNameAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@router.delete("/{cinema_id}/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_room(
    cinema_id: UUID,
    room_id: UUID,
    use_case: Annotated[DeactivateRoom, Depends(get_deactivate_room)],
    _: Annotated[User, Depends(require_admin)],
) -> Response:
    try:
        await use_case.execute(cinema_id, room_id)
    except (CinemaNotFoundError, RoomNotFoundError) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
