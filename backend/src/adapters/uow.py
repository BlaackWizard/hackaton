from dataclasses import dataclass
from typing import Any

from backend.src.application.common.uow import UoW
from sqlalchemy.ext.asyncio import AsyncSession

@dataclass
class UoWImpl(UoW):
    session: AsyncSession

    async def commit(self) -> None:
        await self.session.commit()

    async def add(self, instance: Any) -> None:
        self.session.add(instance)

    async def delete(self, instance: Any) -> None:
        await self.session.delete(instance)
