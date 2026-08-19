from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.users.application.change_password import ChangePassword
from app.users.application.create_user import CreateUser
from app.users.application.get_user_by_id import GetUserById
from app.users.application.list_all_users import ListUsers
from app.users.application.update_user import UpdateUser
from app.users.domain.enums import UserRole
from app.users.domain.exceptions import UserEmailAlreadyExistsError
from app.users.domain.user import User
from app.users.presentation.dependencies import (
    get_change_password,
    get_create_user,
    get_current_user,
    get_list_all_user,
    get_update_user,
    get_user_by_id,
    require_admin,
)
from app.users.presentation.schemas import (
    ChangePasswordRequest,
    ChangePasswordResponse,
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


def to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
    )


@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def list_users(
    use_case: Annotated[ListUsers, Depends(get_list_all_user)],
    _: Annotated[User, Depends(require_admin)],
) -> list[UserResponse]:

    users = await use_case.execute()

    return [to_response(user) for user in users]


@router.get(
    "/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def get_user(
    user_id: UUID,
    use_case: Annotated[GetUserById, Depends(get_user_by_id)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este usuário",
        )

    user = await use_case.execute(user_id)

    return to_response(user)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: CreateUserRequest, use_case: Annotated[CreateUser, Depends(get_create_user)]
) -> UserResponse:
    try:
        user = await use_case.execute(
            name=data.name, email=data.email, password=data.password
        )

    except UserEmailAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(error)
        ) from error

    return to_response(user)


@router.put(
    "/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def update_user(
    user_id: UUID,
    data: UpdateUserRequest,
    use_case: Annotated[UpdateUser, Depends(get_update_user)],
    _: Annotated[User, Depends(require_admin)],
) -> UserResponse:

    user = await use_case.execute(
        user_id=user_id, name=data.name, email=data.email, role=data.role
    )

    return to_response(user)


@router.put(
    "/change_password/{user_id}",
    response_model=ChangePasswordResponse,
    status_code=status.HTTP_200_OK,
)
async def change_password(
    user_id: UUID,
    data: ChangePasswordRequest,
    use_case: Annotated[ChangePassword, Depends(get_change_password)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ChangePasswordResponse:
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode alterar a própria senha",
        )

    await use_case.execute(
        user_id,
        email=data.email,
        new_password=data.new_password,
        new_password_confirmation=data.new_password_confirmation,
    )

    return ChangePasswordResponse(message="Senha Alterada com sucesso")
