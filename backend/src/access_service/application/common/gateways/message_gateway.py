from typing import Protocol
from abc import abstractmethod
from uuid import UUID

from backend.src.access_service.models.message import Message


class MessageGateway(Protocol):
    @abstractmethod
    async def get_message_by_uuid(self, message_id: UUID) -> Message | None: ...
