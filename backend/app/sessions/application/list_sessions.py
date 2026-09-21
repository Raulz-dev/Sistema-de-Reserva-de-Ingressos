from app.sessions.domain.repository import SessionRepository
from app.sessions.domain.session import Session


class ListSessions:
    def __init__(self, repository: SessionRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[Session]:
        return await self._repository.list_sessions()
