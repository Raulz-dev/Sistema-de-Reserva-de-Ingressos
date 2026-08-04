from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import Uuid,func,true
import uuid

class Base(DeclarativeBase):
  pass

class IdMixin:
  id:Mapped[uuid.UUID]= mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)

class TimestampMixin:
  created_at:Mapped[datetime]= mapped_column(server_default=func.now())
  updated_at:Mapped[datetime]= mapped_column(server_default=func.now(), onupdate=func.now())

class IsActiveMixin:
  is_active:Mapped[bool]= mapped_column(default=True,server_default=true())