from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, IdMixin, TimestampMixin
from app.users.domain.enums import UserRole


class UserModel(Base, IdMixin, TimestampMixin):
    __tablename__ = "usuarios"

    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
            values_callable=lambda roles: [role.value for role in roles],
        ),
        default=UserRole.USER,
        nullable=False,
    )

    def __str__(self) -> str:
        return self.name
