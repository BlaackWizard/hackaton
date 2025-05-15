import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

from backend.src.access_service.application.dto import UserIdRequest
from backend.src.access_service.application.graphic_request import GraphicRequest


@pytest.mark.asyncio
async def test_graphic_request_with_data(monkeypatch):
    chat_gateway = AsyncMock()
    user_gateway = AsyncMock()
    user_gateway.get_user_by_id.return_value = MagicMock()

    now = datetime.now()
    chat_gateway.get_all_messages.return_value = [
        {"created_at": (now - timedelta(days=1)).isoformat()},
        {"created_at": (now - timedelta(days=2)).isoformat()},
    ]

    monkeypatch.setattr("your_module.generate_graphic_html", lambda x, y: "/tmp/test.html")

    service = GraphicRequest(chat_gateway, user_gateway)
    result = await service.execute(UserIdRequest(user_id=1))

    assert result == "/tmp/test.html"


@pytest.mark.asyncio
async def test_graphic_request_no_messages():
    chat_gateway = AsyncMock()
    user_gateway = AsyncMock()
    user_gateway.get_user_by_id.return_value = MagicMock()

    chat_gateway.get_all_messages.return_value = []

    service = GraphicRequest(chat_gateway, user_gateway)
    result = await service.execute(UserIdRequest(user_id=1))

    assert result == "Нет сообщений"
