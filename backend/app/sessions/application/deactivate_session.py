from uuid import UUID

from app.sessions.domain.exceptions import SessionNotFoundError
from app.sessions.domain.repository import SessionRepository


class DeactivateSession:
    def __init__(self, repository: SessionRepository) -> None:
        self._repository = repository

    async def execute(self, session_id: UUID) -> None:
        session = await self._repository.find_session_by_id(session_id)
        if session is None:
            raise SessionNotFoundError("Sessão não encontrada.")
        session.deactivate()
        await self._repository.update_session(session)
