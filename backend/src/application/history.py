from dataclasses import dataclass

from backend.src.application.common.gateways.chat_gateway import ChatGateway
from backend.src.application.dto import UserIdRequest
from backend.src.models.chat import Chat
from backend.src.models.message import Message


@dataclass
class History:
    chat_gateway: ChatGateway


    async def execute(self, data: UserIdRequest) -> list[dict]:
        response = await self.chat_gateway.get_all_messages(data.user_id)

        return response
