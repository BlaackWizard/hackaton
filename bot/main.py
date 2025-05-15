import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

from bot.handlers import frequest_requests
from handlers.frequest_requests import router
from keyboards.interactor_keyboard import actions_kb

env_path = Path(__file__).parent / ".env"

load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Добро пожаловать! Пишите ваш запрос или жалобу. Вот список команд:", reply_markup=actions_kb)


async def main():
    bot = Bot(token=BOT_TOKEN)

    dp.include_router(frequest_requests.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
