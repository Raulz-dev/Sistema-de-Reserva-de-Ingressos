from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.users.application.create_user import CreateUser
from app.users.domain.exceptions import UserEmailAlreadyExistsError
from app.users.presentation.dependencies import get_create_user
from app.users.presentation.schemas import (
    CreateUserRequest,
    CreateUserResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: CreateUserRequest, use_case: Annotated[CreateUser, Depends(get_create_user)]
) -> CreateUserResponse:
    try:
        user = await use_case.execute(
            name=data.name, email=data.email, password=data.password
        )

    except UserEmailAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(error)
        ) from error

    return CreateUserResponse(
        id=user.id, name=user.name, email=user.email, role=user.role
    )
