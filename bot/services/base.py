import os
from pathlib import Path

import aiohttp
from dotenv import load_dotenv

MAX_MESSAGE_LENGTH = 4096

class BaseService:
    def __init__(self):
        self.load_env()
        self.base_url = os.getenv("BASE_URL", "http://localhost:8000")

    def load_env(self):
        env_path = Path(__file__).parent / ".env"
        load_dotenv(dotenv_path=env_path)

    async def request_get(self, url, params=None):
        async with aiohttp.ClientSession() as client:
            async with client.get(url, params=params) as response:
                return response.status, await response.text(), response

    async def request_post(self, url, params=None, json_payload=None):
        async with aiohttp.ClientSession() as client:
            async with client.post(url, params=params, json=json_payload) as response:
                return response.status, await response.text()

    def split_message(self, text: str, max_length: int = MAX_MESSAGE_LENGTH):
        parts = []
        while len(text) > max_length:
            split_index = text.rfind("\n", 0, max_length)
            if split_index == -1:
                split_index = max_length
            parts.append(text[:split_index])
            text = text[split_index:].lstrip()
        parts.append(text)
        return parts
