from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.src.access_service.models.user import User
from backend.src.access_service.application.common.gateways.user_gateway import UserGateway


@dataclass
class UserGatewayImpl(UserGateway):
    session: AsyncSession

    async def get_user_by_id(self, user_id: int) -> User | None:
        q = select(User).where(User.user_id == user_id)
        result = await self.session.execute(q)
        user = result.scalar_one_or_none()
        return user

