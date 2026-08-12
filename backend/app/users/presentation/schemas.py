from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.users.domain.enums import UserRole


class CreateUserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=12)


class ListAllUsersResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole
