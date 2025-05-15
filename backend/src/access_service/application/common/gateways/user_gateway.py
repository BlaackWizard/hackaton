from typing import Protocol
from abc import abstractmethod

from backend.src.access_service.models.user import User


class UserGateway(Protocol):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None: ...
