from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.sessions.domain.session import Session


class SessionRepository(Protocol):
    async def create_session(self, session: Session) -> Session: ...

    async def find_session_by_id(self, session_id: UUID) -> Session | None: ...

    async def list_sessions(self) -> list[Session]: ...

    async def has_room_conflict(
        self,
        room_id: UUID,
        starts_at: datetime,
        ends_at: datetime,
        exclude_session_id: UUID | None = None,
    ) -> bool: ...

    async def update_session(self, session: Session) -> Session: ...
