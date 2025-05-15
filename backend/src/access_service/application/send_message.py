import uuid
from dataclasses import dataclass
from datetime import datetime

from backend.src.access_service.application.common.ai_model import AiModel
from backend.src.access_service.application.common.gateways.message_gateway import MessageGateway
from backend.src.access_service.application.common.gateways.user_gateway import UserGateway
from backend.src.access_service.application.common.uow import UoW
from backend.src.access_service.application.dto import NewMessageSendRequest
from backend.src.access_service.application.exceptions.user import NotFoundUserError
from backend.src.access_service.models.chat import Chat
from backend.src.access_service.models.message import Message
from backend.src.access_service.models.user import User


@dataclass
class SendMessage:
    message_gateway: MessageGateway
    uow: UoW
    user_gateway: UserGateway
    ai_model: AiModel

    async def execute(self, data: NewMessageSendRequest) -> str | None:
        user = await self.user_gateway.get_user_by_id(data.user_id)

        if not user:
            chat_id = uuid.uuid4()
            chat = Chat(chat_id=chat_id, created_at=datetime.now())
            await self.uow.add(chat)

            user = User(user_id=data.user_id, chat_id=chat_id)
            await self.uow.add(user)
            await self.uow.commit()

        message = Message(
            user_id=user.user_id,
            content=data.content,
            created_at=datetime.now(),
            chat_id=user.chat_id,
            message_id=uuid.uuid4()
        )

        message.ai_response = await self.ai_model.generate_text(message)

        await self.uow.add(message)
        await self.uow.commit()

        return str(message.ai_response)
