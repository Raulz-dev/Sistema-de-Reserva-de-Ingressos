from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.users.application.create_user import CreateUser
from app.users.application.list_all_users import ListUsers
from app.users.application.update_user import UpdateUser
from app.users.domain.exceptions import UserEmailAlreadyExistsError
from app.users.presentation.dependencies import (
    get_create_user,
    get_list_all_user,
    get_update_user,
)
from app.users.presentation.schemas import (
    CreateUserRequest,
    CreateUserResponse,
    ListAllUsersResponse,
    UpdateUserRequest,
    UpdateUserResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "", response_model=list[ListAllUsersResponse], status_code=status.HTTP_200_OK
)
async def list_users(
    use_case: Annotated[ListUsers, Depends(get_list_all_user)],
) -> list[ListAllUsersResponse]:

    users = await use_case.execute()

    return [
        ListAllUsersResponse(
            id=user.id, name=user.name, email=user.email, role=user.role
        )
        for user in users
    ]


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


@router.put(
    "/{user_id}", response_model=UpdateUserResponse, status_code=status.HTTP_200_OK
)
async def update_user(
    user_id: UUID,
    data: UpdateUserRequest,
    use_case: Annotated[UpdateUser, Depends(get_update_user)],
) -> UpdateUserResponse:

    user = await use_case.execute(
        user_id=user_id, name=data.name, email=data.email, role=data.role
    )

    return UpdateUserResponse(
        id=user_id, name=user.name, email=user.email, role=user.role
    )
