import datetime
import uuid
from dataclasses import dataclass

from backend.src.application.common.gateways.chat_gateway import ChatGateway
from backend.src.application.common.gateways.user_gateway import UserGateway
from backend.src.application.common.uow import UoW
from backend.src.application.dto import NewChatUserIdRequest, UserIdRequest
from backend.src.application.exceptions.user import NotFoundUserError
from backend.src.models.chat import Chat
from datetime import datetime

from backend.src.models.user import User


@dataclass
class NewChat:
    chat_gateway: ChatGateway
    user_gateway: UserGateway
    uow: UoW

    async def execute(self, data: UserIdRequest) -> None:
        chat_id = uuid.uuid4()
        created_at = datetime.now()

        chat = Chat(
            chat_id=chat_id,
            created_at=created_at
        )
        await self.uow.add(chat)

        user = await self.user_gateway.get_user_by_id(data.user_id)
        if not user:
            raise NotFoundUserError

        user.chat_id = chat_id

        await self.uow.add(user)
        await self.uow.commit()

        return
