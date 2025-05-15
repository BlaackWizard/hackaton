import json

from bot.services.base import BaseService

from aiogram.types import Message

class FrequentRequestService(BaseService):
    async def handle(self, message: Message):
        try:
            status, text, _ = await self.request_get(
                f"{self.base_url}/energy-insight/frequent-requests",
                params={"user_id": message.from_user.id}
            )
            if status != 200:
                await message.answer(f"Ошибка: {text}")
                return

            try:
                data = json.loads(text)
                if isinstance(data, list):
                    formatted = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(data)])
                elif isinstance(data, str):
                    lines = [line.strip().strip('"') for line in data.split('\n') if line.strip()]
                    formatted = "\n".join([f"{i + 1}. {line}" for i, line in enumerate(lines)])
                elif isinstance(data, dict):
                    summary = data.get("summary")
                    if summary:
                        formatted = f"<i>{summary}</i>"
                    else:
                        formatted = "\n".join([f"<b>{key.capitalize()}:</b> {value}" for key, value in data.items()])
                else:
                    formatted = f"Данные с сервера не распознаны. {data}"

                await message.answer(f"<b>Часто задаваемые вопросы:</b>\n\n{formatted}", parse_mode="HTML")
            except json.JSONDecodeError:
                await message.answer("не форматируется в json")
        except Exception as e:
            await message.answer(f"Error: {e}")
