from typing import Protocol
from abc import abstractmethod

from backend.src.access_service.models.message import Message


class AiModel(Protocol):
    @abstractmethod
    async def generate_text(self, message: Message) -> str: ...
