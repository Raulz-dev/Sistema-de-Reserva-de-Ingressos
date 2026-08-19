from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.users.domain.enums import UserRole


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=12)


class UpdateUserRequest(BaseModel):
    name: str | None = Field(min_length=2, max_length=100)
    email: EmailStr | None = None
    role: UserRole | None = None


class ChangePasswordRequest(BaseModel):
    email: EmailStr
    new_password: str = Field(min_length=8, max_length=128)
    new_password_confirmation: str = Field(
        min_length=8,
        max_length=128,
    )


class ChangePasswordResponse(BaseModel):
    message: str


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str


class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
