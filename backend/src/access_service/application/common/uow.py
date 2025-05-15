from typing import Protocol, Any
from abc import abstractmethod

class UoW(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def add(self, instance: Any) -> None: ...

    @abstractmethod
    async def delete(self, instance: Any) -> None: ...
