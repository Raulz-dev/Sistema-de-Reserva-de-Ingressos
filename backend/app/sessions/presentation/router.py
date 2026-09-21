from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.sessions.application.create_session import CreateSession
from app.sessions.application.deactivate_session import DeactivateSession
from app.sessions.application.get_session import GetSession
from app.sessions.application.list_sessions import ListSessions
from app.sessions.application.update_session import UpdateSession
from app.sessions.domain.exceptions import (
    InvalidSessionError,
    SessionConflictError,
    SessionMovieNotFoundError,
    SessionNotFoundError,
    SessionRoomNotFoundError,
)
from app.sessions.domain.session import Session
from app.sessions.presentation.dependencies import (
    get_create_session,
    get_deactivate_session,
    get_list_sessions,
    get_session,
    get_update_session,
)
from app.sessions.presentation.schemas import (
    CreateSessionRequest,
    SessionResponse,
    UpdateSessionRequest,
)
from app.users.domain.user import User
from app.users.presentation.dependencies import require_admin

router = APIRouter(prefix="/sessions", tags=["Sessions"])


def session_to_response(session: Session) -> SessionResponse:
    return SessionResponse(
        id=session.id,
        movie_id=session.movie_id,
        room_id=session.room_id,
        starts_at=session.starts_at,
        ends_at=session.ends_at,
        price=session.price,
        is_active=session.is_active,
    )


def raise_session_http_error(error: Exception) -> None:
    if isinstance(error, (SessionMovieNotFoundError, SessionRoomNotFoundError)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    if isinstance(error, SessionConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    data: CreateSessionRequest,
    use_case: Annotated[CreateSession, Depends(get_create_session)],
    _: Annotated[User, Depends(require_admin)],
) -> SessionResponse:
    try:
        return session_to_response(await use_case.execute(**data.model_dump()))
    except (
        InvalidSessionError,
        SessionConflictError,
        SessionMovieNotFoundError,
        SessionRoomNotFoundError,
    ) as error:
        raise_session_http_error(error)


@router.get("", response_model=list[SessionResponse])
async def list_sessions(
    use_case: Annotated[ListSessions, Depends(get_list_sessions)],
) -> list[SessionResponse]:
    return [session_to_response(item) for item in await use_case.execute()]


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session_by_id(
    session_id: UUID,
    use_case: Annotated[GetSession, Depends(get_session)],
) -> SessionResponse:
    try:
        return session_to_response(await use_case.execute(session_id))
    except SessionNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: UUID,
    data: UpdateSessionRequest,
    use_case: Annotated[UpdateSession, Depends(get_update_session)],
    _: Annotated[User, Depends(require_admin)],
) -> SessionResponse:
    try:
        return session_to_response(
            await use_case.execute(session_id, **data.model_dump())
        )
    except SessionNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except (
        InvalidSessionError,
        SessionConflictError,
        SessionMovieNotFoundError,
        SessionRoomNotFoundError,
    ) as error:
        raise_session_http_error(error)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_session(
    session_id: UUID,
    use_case: Annotated[DeactivateSession, Depends(get_deactivate_session)],
    _: Annotated[User, Depends(require_admin)],
) -> Response:
    try:
        await use_case.execute(session_id)
    except SessionNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)
