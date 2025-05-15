import json

from bot.services.base import BaseService
from aiogram.types import Message

class ProblemTypeService(BaseService):
    async def handle(self, message: Message):
        try:
            status, text, _ = await self.request_get(
                f"{self.base_url}/energy-insight/problem-type",
                params={"user_id": message.from_user.id}
            )
            if status != 200:
                await message.answer(f"Ошибка: {text}")
                return
            try:
                data = json.loads(text)
                categories = data.get("categories", "")
                formatted = "\n".join(
                    f"- {k.strip()}: {v.strip()}"
                    for line in categories.split("\n") if ":" in line
                    for k, v in [line.split(":", 1)]
                )
                await message.answer(f"категории проблем:\n{formatted}")
            except json.JSONDecodeError:
                await message.answer("ошибка разбора категорий.")
        except Exception as e:
            await message.answer(f"ошибка: {e}")
