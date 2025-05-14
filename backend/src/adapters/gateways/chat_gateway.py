from uuid import UUID

from backend.src.application.common.gateways.chat_gateway import ChatGateway
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from backend.src.models.chat import Chat
from backend.src.models.message import Message
from dataclasses import dataclass

@dataclass
class ChatGatewayImpl(ChatGateway):
    session: AsyncSession

    async def get_chat_by_uuid(self, chat_id: UUID) -> Chat | None:
        q = select(Chat).where(Chat.chat_id == chat_id)

        result = await self.session.execute(q)

        chat = result.scalar_one_or_none()

        return chat

    async def get_all_messages(self, user_id: int) -> list[dict]:
        q = select(Message).where(Message.user_id == user_id).order_by(Message.created_at)

        result = await self.session.execute(q)
        messages = result.scalars().all()

        return [
            {
                "message": str(msg.message_id),
                "content": msg.content,
                "ai_response": msg.ai_response,
                "created_at": msg.created_at.isoformat(),
                "chat_id": str(msg.chat_id)
            }
            for msg in messages
        ]
