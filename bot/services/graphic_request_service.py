import aiohttp

from bot.services.base import BaseService
from aiogram.types import Message, BufferedInputFile

class GraphicRequestService(BaseService):
    async def handle(self, message: Message):
        try:
            async with aiohttp.ClientSession() as client:
                async with client.get(
                    f"{self.base_url}/energy-insight/graphic-requests",
                    params={"user_id": message.from_user.id}
                ) as response:
                    content = await response.read()
                    if response.headers.get("Content-Type") == "text/plain; charset=utf-8":
                        await message.answer(content.decode('utf-8'))
                    else:
                        document = BufferedInputFile(content, filename="graphic.html")
                        await message.reply_document(document, caption="График запросов за последние 30 дней")
        except Exception as e:
            await message.answer(f"ошибка: {e}")
