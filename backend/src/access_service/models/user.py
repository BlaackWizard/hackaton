from uuid import UUID

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Uuid

from backend.src.access_service.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    chat_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
