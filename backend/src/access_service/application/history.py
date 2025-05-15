from dataclasses import dataclass

from backend.src.access_service.application.common.gateways.chat_gateway import ChatGateway
from backend.src.access_service.application.dto import UserIdRequest
from backend.src.access_service.models.chat import Chat
from backend.src.access_service.models.message import Message


@dataclass
class History:
    chat_gateway: ChatGateway


    async def execute(self, data: UserIdRequest) -> list[dict]:
        response = await self.chat_gateway.get_all_messages(data.user_id)

        return response
