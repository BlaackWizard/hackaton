from sqlalchemy import Uuid
from sqlalchemy.orm import mapped_column, Mapped

from uuid import UUID
from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    chat_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
