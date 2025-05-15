import uuid
from collections import Counter
from datetime import datetime, timedelta
from dataclasses import dataclass

from backend.src.access_service.application.common.gateways.chat_gateway import ChatGateway
from backend.src.access_service.application.common.gateways.user_gateway import UserGateway
from backend.src.access_service.application.common.graphic_generate_html import generate_graphic_html
from backend.src.access_service.application.common.uow import UoW
from backend.src.access_service.application.dto import UserIdRequest
from backend.src.access_service.application.exceptions.user import NotFoundUserError
from backend.src.access_service.models.chat import Chat
from backend.src.access_service.models.user import User


@dataclass
class GraphicRequest:
    chat_gateway: ChatGateway
    user_gateway: UserGateway
    uow: UoW
    async def execute(self, data: UserIdRequest) -> bytes | str:
        user = await self.user_gateway.get_user_by_id(data.user_id)
        if not user:
            chat_id = uuid.uuid4()
            chat = Chat(chat_id=chat_id, created_at=datetime.now())
            await self.uow.add(chat)

            user = User(user_id=data.user_id, chat_id=chat_id)
            await self.uow.add(user)
            await self.uow.commit()

        raw_messages = await self.chat_gateway.get_all_messages(data.user_id)

        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)

        recent_messages = [
            msg for msg in raw_messages
            if "created_at" in msg and datetime.fromisoformat(msg["created_at"]) >= thirty_days_ago
        ]

        if not recent_messages:
            return 'Нет сообщений за последние 30 дней'

        date_counts = Counter(
            datetime.fromisoformat(msg["created_at"]).date().isoformat()
            for msg in recent_messages
        )

        days = [(now - timedelta(days=i)).date().isoformat() for i in range(29, -1, -1)]
        counts = [date_counts.get(day, 0) for day in days]

        html_bytes = generate_graphic_html(x=days, y=counts)
        return html_bytes

