from backend.src.access_service.models.message import Message
from bot.services.base import BaseService
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message

class MessageSendService(BaseService):
    async def handle(self, message: Message):
        try:
            payload = {
                "content": message.text,
                "user_id": message.from_user.id
            }
            status, text = await self.request_post(
                f"{self.base_url}/energy-insight/send-message",
                json_payload=payload
            )
            text = text.replace('"', '')
            await message.answer(text if status == 200 else f"Ошибка: {text}", parse_mode=ParseMode.HTML)
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
