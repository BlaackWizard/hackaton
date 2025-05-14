from dataclasses import dataclass
from datetime import datetime, timedelta

from backend.src.application.common.ai_model import AiModel
from backend.src.application.common.gateways.chat_gateway import ChatGateway
from backend.src.application.dto import UserIdRequest
from backend.src.models.message import Message


@dataclass
class ProblemType:
    chat_gateway: ChatGateway

    ai_model: AiModel

    async def execute(self, data: UserIdRequest) -> dict:
        raw_messages = await self.chat_gateway.get_all_messages(data.user_id)

        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)

        recent_messages = [
            msg for msg in raw_messages
            if "created_at" in msg and datetime.fromisoformat(msg["created_at"]) >= thirty_days_ago
        ]

        if not recent_messages:
            return {"categories": "Нет сообщений за последние 30 дней."}

        message_texts = [msg["content"] for msg in recent_messages if "content" in msg]
        combined_text = "\n".join(f"- {text}" for text in message_texts)

        system_prompt = (
            "Проанализируй следующие сообщения пользователя и определи, какие типы проблем или категорий в них встречаются. "
            "Верни результат в формате:\n\n"
            "Категория: Количество сообщений\n"
            "Пример: \n"
            "Технические проблемы: 5\n"
            "Вопросы по оплате: 3\n"
            "Регистрация аккаунта: 2\n"
        )

        full_input = f"{system_prompt}\n\n{combined_text}"

        fake_message = Message(
            id=0,
            user_id=data.user_id,
            content=full_input,
            ai_response=None,
            created_at=now,
            chat_id=0  #
        )

        categories_result = await self.ai_model.generate_text(fake_message)

        return {"categories": categories_result}
