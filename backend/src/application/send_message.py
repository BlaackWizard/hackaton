import uuid
from dataclasses import dataclass
from datetime import datetime

from backend.src.application.common.ai_model import AiModel
from backend.src.application.common.gateways.message_gateway import MessageGateway
from backend.src.application.common.gateways.user_gateway import UserGateway
from backend.src.application.common.uow import UoW
from backend.src.application.dto import NewMessageSendRequest
from backend.src.application.exceptions.user import NotFoundUserError
from backend.src.models.message import Message


@dataclass
class SendMessage:
    message_gateway: MessageGateway
    uow: UoW
    user_gateway: UserGateway
    ai_model: AiModel

    async def execute(self, data: NewMessageSendRequest) -> str | None:
        user = await self.user_gateway.get_user_by_id(data.user_id)

        if not user:
            raise NotFoundUserError

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
