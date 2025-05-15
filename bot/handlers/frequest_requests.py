import json
import os
from datetime import datetime
from pathlib import Path

import aiohttp
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.input_file import BufferedInputFile
from dotenv import load_dotenv

router = Router()

MAX_MESSAGE_LENGTH = 4096

def load_data():
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path)


def get_base_url():
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    return BASE_URL


@router.message(Command('frequent_request_handler'))
async def frequent_request_handler(message: Message):
    try:
        load_data()
        BASE_URL = get_base_url()

        async with aiohttp.ClientSession() as client:
            async with client.get(
                f"{BASE_URL}/energy-insight/frequent-requests",
                params={"user_id": message.from_user.id}
            ) as response:
                text = await response.text()

                if response.status != 200:
                    await message.answer(f"Ошибка: {text}")
                    return

                try:
                    data = json.loads(text)
                    if isinstance(data, list):
                        formatted = "\n".join(
                            [f"{i+1}. {item}" for i, item in enumerate(data)]
                        )
                    elif isinstance(data, str):
                        lines = [line.strip().strip('"') for line in data.split('\n') if line.strip()]
                        formatted = "\n".join(
                            [f"{i+1}. {line}" for i, line in enumerate(lines)]
                        )
                    else:
                        formatted = "Данные с сервера не распознаны."

                    await message.answer(f"<b>Часто задаваемые вопросы:</b>\n\n{formatted}", parse_mode="HTML")

                except json.JSONDecodeError:
                    await message.answer("не форматируется в json")
    except Exception as e:
        await message.answer(f"Error: {e}")


def split_message(text: str, max_length: int = MAX_MESSAGE_LENGTH):
    parts = []
    while len(text) > max_length:
        split_index = text.rfind("\n", 0, max_length)
        if split_index == -1:
            split_index = max_length
        parts.append(text[:split_index])
        text = text[split_index:].lstrip()
    parts.append(text)
    return parts


@router.message(Command("history"))
async def history_handler(message: Message):
    try:
        BASE_URL = get_base_url()

        async with aiohttp.ClientSession() as client:
            async with client.get(
                    f"{BASE_URL}/energy-insight/history",
                    params={"user_id": message.from_user.id}
            ) as response:

                text = await response.text()

                if response.status != 200:
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

                formatted_messages = []
                for item in messages:
                    created_at = datetime.fromisoformat(item["created_at"]).strftime("%d.%m.%Y %H:%M")
                    formatted_messages.append(
                        f"📅 <b>{created_at}</b>\n"
                        f"🧑‍💬 <b>Вы:</b> {item['content']}\n"
                        f"🤖 <b>AI:</b> {item['ai_response']}"
                    )

                reply_text = "\n\n".join(formatted_messages)

                # Разбиваем длинное сообщение на части
                parts = split_message(reply_text)
                for part in parts:
                    await message.answer(part, parse_mode="HTML")

    except EnvironmentError as e:
        await message.answer(str(e))
    except aiohttp.ClientError as e:
        await message.answer(f"Ошибка соединения с сервером: {e}")
    except Exception as e:
        await message.answer(f"Неожиданная ошибка: {e}")


@router.message(Command("new_chat"))
async def new_chat_handler(message: Message):
    try:
        load_data()
        BASE_URL = get_base_url()

        async with aiohttp.ClientSession() as client:
            async with client.post(f"{BASE_URL}/energy-insight/new-chat", params={"user_id": message.from_user.id}) as response:
                text = await response.text()
                await message.answer("Чат создан" if response.status == 200 else f"Ошибка: {text}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


@router.message(Command("type_problems"))
async def problem_type_handler(message: Message):
    try:
        BASE_URL = get_base_url()

        async with aiohttp.ClientSession() as client:
            async with client.get(f"{BASE_URL}/energy-insight/problem-type", params={"user_id": message.from_user.id}) as response:
                text = await response.text()

                if response.status != 200:
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
                    await message.answer(f"Категории проблем:\n{formatted}")
                except json.JSONDecodeError:
                    await message.answer("Ошибка разбора категорий.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


@router.message(Command("graphic_requests"))
async def graphic_requests(message: Message):
    try:
        load_data()
        BASE_URL = get_base_url()

        async with aiohttp.ClientSession() as client:
            async with client.get(
                f"{BASE_URL}/energy-insight/graphic-requests",
                params={"user_id": message.from_user.id}
            ) as response:

                content = await response.read()

                if response.headers.get("Content-Type") == "text/plain; charset=utf-8":
                    text = content.decode('utf-8')
                    await message.answer(text)
                    return

                document = BufferedInputFile(content, filename="graphic.html")
                await message.reply_document(document, caption="График запросов за последние 30 дней")

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

@router.message(F.text)
async def send_message_handler(message: Message):
    try:
        load_data()
        BASE_URL = get_base_url()

        payload = {
            "content": message.text,
            "user_id": message.from_user.id
        }

        async with aiohttp.ClientSession() as client:
            async with client.post(f"{BASE_URL}/energy-insight/send-message", json=payload) as response:
                text = await response.text()
                await message.answer(text if response.status == 200 else f"Ошибка: {text}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
