from dataclasses import dataclass
from datetime import datetime, timedelta

from backend.src.application.common.ai_model import AiModel
from backend.src.application.common.gateways.chat_gateway import ChatGateway
from backend.src.application.dto import UserIdRequest
from backend.src.models.message import Message


@dataclass
class FrequentRequests:
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
            return {"summary": "Нет сообщений за последние 30 дней."}

        message_texts = [msg["content"] for msg in recent_messages if "content" in msg]

        combined_text = "\n".join(f"- {text}" for text in message_texts)

        system_prompt = (
            f"""
            Ответь коротким текстом около 3-4 предложения, И отвечай прямо мне а не от 3-лица, ответь красивыми строками 
            Посмотри на сообщения людей, найди те, которые похожи друг на друга или часто повторяются. 
            Затем раздели их на группы, чтобы было понятно, чего хотят люди. Представь результат как список общих тем или желаний.\n\nТеперь даже маленькие дети смогут понять суть! 😊
            """
        )
        full_input = f"{system_prompt}\n\n{combined_text}"

        fake_message = Message(
            id=0,
            user_id=data.user_id,
            content=full_input,
            ai_response=None,
            created_at=now,
            chat_id=0
        )

        summary = await self.ai_model.generate_text(fake_message)

        return {"summary": summary}
