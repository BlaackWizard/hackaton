from typing import Protocol
from abc import abstractmethod
from uuid import UUID

from backend.src.models.chat import Chat
from backend.src.models.message import Message


class ChatGateway(Protocol):
    @abstractmethod
    async def get_chat_by_uuid(self, chat_id: UUID) -> Chat | None: ...

    @abstractmethod
    async def get_all_messages(self, user_id: int) -> list[dict]: ...

