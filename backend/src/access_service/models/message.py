from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Uuid, DateTime, ForeignKey

from backend.src.access_service.models.base import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    message_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    ai_response: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    chat_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("chats.chat_id"))
