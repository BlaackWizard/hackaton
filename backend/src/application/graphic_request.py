from collections import Counter
from datetime import datetime, timedelta
from dataclasses import dataclass

from backend.src.application.common.gateways.chat_gateway import ChatGateway
from backend.src.application.common.gateways.user_gateway import UserGateway
from backend.src.application.common.graphic_generate_html import generate_graphic_html
from backend.src.application.dto import UserIdRequest
from backend.src.application.exceptions.user import NotFoundUserError


@dataclass
class GraphicRequest:
    chat_gateway: ChatGateway
    user_gateway: UserGateway

    async def execute(self, data: UserIdRequest) -> str:
        user = await self.user_gateway.get_user_by_id(data.user_id)
        if not user:
            raise NotFoundUserError

        raw_messages = await self.chat_gateway.get_all_messages(data.user_id)

        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)

        recent_messages = [
            msg for msg in raw_messages
            if "created_at" in msg and datetime.fromisoformat(msg["created_at"]) >= thirty_days_ago
        ]

        if not recent_messages:
            return 'Нет сообщений'

        # Считаем количество сообщений по датам (только день, без времени)
        date_counts = Counter(
            datetime.fromisoformat(msg["created_at"]).date().isoformat()
            for msg in recent_messages
        )

        # Гарантируем, что каждый из 30 дней присутствует, даже с нулём
        days = [(now - timedelta(days=i)).date().isoformat() for i in range(29, -1, -1)]
        counts = [date_counts.get(day, 0) for day in days]

        output_path = generate_graphic_html(x=days, y=counts)

        return output_path
