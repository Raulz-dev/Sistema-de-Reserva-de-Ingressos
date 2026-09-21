from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cinemas.domain.cinema import Cinema
from app.cinemas.domain.repository import CinemaRepository, RoomRepository
from app.cinemas.domain.room import Room
from app.cinemas.infrastructure.models import CinemaModel, RoomModel


class SQLAlchemyCinemaRepository(CinemaRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_cinema(self, cinema: Cinema) -> Cinema:
        model = self._to_model(cinema)
        self._db.add(model)
        await self._db.commit()
        await self._db.refresh(model)
        return self._to_domain(model)

    async def find_cinema_by_id(self, cinema_id: UUID) -> Cinema | None:
        model = await self._db.scalar(
            select(CinemaModel).where(
                CinemaModel.id == cinema_id, CinemaModel.is_active.is_(True)
            )
        )
        return None if model is None else self._to_domain(model)

    async def find_cinema_by_name(self, name: str) -> Cinema | None:
        model = await self._db.scalar(select(CinemaModel).where(CinemaModel.name == name))
        return None if model is None else self._to_domain(model)

    async def list_cinemas(self) -> list[Cinema]:
        result = await self._db.scalars(
            select(CinemaModel)
            .where(CinemaModel.is_active.is_(True))
            .order_by(CinemaModel.name)
        )
        return [self._to_domain(model) for model in result.all()]

    async def update_cinema(self, cinema: Cinema) -> Cinema:
        model = await self._db.get(CinemaModel, cinema.id)
        if model is None:
            return cinema

        model.name = cinema.name
        model.street = cinema.street
        model.number = cinema.number
        model.complement = cinema.complement
        model.neighborhood = cinema.neighborhood
        model.zip_code = cinema.zip_code
        model.is_active = cinema.is_active
        await self._db.commit()
        await self._db.refresh(model)
        return self._to_domain(model)

    @staticmethod
    def _to_model(cinema: Cinema) -> CinemaModel:
        return CinemaModel(
            id=cinema.id,
            name=cinema.name,
            street=cinema.street,
            number=cinema.number,
            complement=cinema.complement,
            neighborhood=cinema.neighborhood,
            zip_code=cinema.zip_code,
            is_active=cinema.is_active,
        )

    @staticmethod
    def _to_domain(model: CinemaModel) -> Cinema:
        return Cinema(
            id=model.id,
            name=model.name,
            street=model.street,
            number=model.number,
            complement=model.complement,
            neighborhood=model.neighborhood,
            zip_code=model.zip_code,
            is_active=model.is_active,
        )


class SQLAlchemyRoomRepository(RoomRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_room(self, room: Room) -> Room:
        model = self._to_model(room)
        self._db.add(model)
        await self._db.commit()
        await self._db.refresh(model)
        return self._to_domain(model)

    async def find_room_by_id(self, cinema_id: UUID, room_id: UUID) -> Room | None:
        model = await self._db.scalar(
            select(RoomModel).where(
                RoomModel.id == room_id,
                RoomModel.cinema_id == cinema_id,
                RoomModel.is_active.is_(True),
            )
        )
        return None if model is None else self._to_domain(model)

    async def find_active_room_by_id(self, room_id: UUID) -> Room | None:
        model = await self._db.scalar(
            select(RoomModel).where(
                RoomModel.id == room_id, RoomModel.is_active.is_(True)
            )
        )
        return None if model is None else self._to_domain(model)

    async def find_room_by_name(self, cinema_id: UUID, name: str) -> Room | None:
        model = await self._db.scalar(
            select(RoomModel).where(
                RoomModel.cinema_id == cinema_id, RoomModel.name == name
            )
        )
        return None if model is None else self._to_domain(model)

    async def list_rooms(self, cinema_id: UUID) -> list[Room]:
        result = await self._db.scalars(
            select(RoomModel)
            .where(RoomModel.cinema_id == cinema_id, RoomModel.is_active.is_(True))
            .order_by(RoomModel.name)
        )
        return [self._to_domain(model) for model in result.all()]

    async def update_room(self, room: Room) -> Room:
        model = await self._db.get(RoomModel, room.id)
        if model is None:
            return room

        model.name = room.name
        model.row_count = room.row_count
        model.seats_per_row = room.seats_per_row
        model.is_active = room.is_active
        await self._db.commit()
        await self._db.refresh(model)
        return self._to_domain(model)

    @staticmethod
    def _to_model(room: Room) -> RoomModel:
        return RoomModel(
            id=room.id,
            cinema_id=room.cinema_id,
            name=room.name,
            row_count=room.row_count,
            seats_per_row=room.seats_per_row,
            is_active=room.is_active,
        )

    @staticmethod
    def _to_domain(model: RoomModel) -> Room:
        return Room(
            id=model.id,
            cinema_id=model.cinema_id,
            name=model.name,
            row_count=model.row_count,
            seats_per_row=model.seats_per_row,
            is_active=model.is_active,
        )
