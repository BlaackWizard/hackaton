from dataclasses import dataclass
from uuid import UUID

from backend.src.access_service.application.common.gateways.message_gateway import MessageGateway
from backend.src.access_service.models.message import Message
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass

@dataclass
class MessageGatewayImpl(MessageGateway):
    session: AsyncSession

    async def get_message_by_uuid(self, message_id: UUID) -> Message | None:
        q = select(Message).where(Message.message_id == message_id)

        res = await self.session.execute(q)
        message = res.scalar_one_or_none()
        return message
