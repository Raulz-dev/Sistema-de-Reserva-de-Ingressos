from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.users.application.login_user import Login
from app.users.domain.exceptions import InvalidCredentialsError
from app.users.presentation.dependencies import get_login_user
from app.users.presentation.schemas import LoginUserRequest, LoginUserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login", response_model=LoginUserResponse, status_code=status.HTTP_200_OK
)
async def login(
    data: LoginUserRequest, use_case: Annotated[Login, Depends(get_login_user)]
) -> LoginUserResponse:
    try:
        access_token = await use_case.execute(data.email, data.password)
    except InvalidCredentialsError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    return LoginUserResponse(access_token=access_token)
