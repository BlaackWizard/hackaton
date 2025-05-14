from datetime import datetime
from uuid import UUID

from sqlalchemy import Uuid, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from backend.src.models.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    chat_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
