import json
from datetime import datetime

from bot.services.base import BaseService

from aiogram.types import Message

class HistoryService(BaseService):
    async def handle(self, message: Message):
        try:
            status, text, _ = await self.request_get(
                f"{self.base_url}/energy-insight/history",
                params={"user_id": message.from_user.id}
            )
            if status != 200:
                await message.answer(f"Ошибка: {text}")
                return

            try:
                messages = json.loads(text)
            except json.JSONDecodeError:
                await message.answer("Ошибка при разборе ответа сервера.")
                return

            if not messages:
                await message.answer("История сообщений пуста.")
                return

            formatted = []
            for item in messages:
                created_at = datetime.fromisoformat(item["created_at"]).strftime("%d.%m.%Y %H:%M")
                formatted.append(
                    f"📅 <b>{created_at}</b>\n🧑‍💬 <b>Вы:</b> {item['content']}\n🤖 <b>AI:</b> {item['ai_response']}"
                )
            for part in self.split_message("\n\n".join(formatted)):
                await message.answer(part, parse_mode="HTML")
        except Exception as e:
            await message.answer(f"ошибка: {e}")
