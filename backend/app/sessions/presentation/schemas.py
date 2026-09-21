from decimal import Decimal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, Field


class SessionResponse(BaseModel):
    id: UUID
    movie_id: UUID
    room_id: UUID
    starts_at: AwareDatetime
    ends_at: AwareDatetime
    price: Decimal
    is_active: bool


class CreateSessionRequest(BaseModel):
    movie_id: UUID
    room_id: UUID
    starts_at: AwareDatetime
    ends_at: AwareDatetime
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class UpdateSessionRequest(BaseModel):
    movie_id: UUID | None = None
    room_id: UUID | None = None
    starts_at: AwareDatetime | None = None
    ends_at: AwareDatetime | None = None
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
