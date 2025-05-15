import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

from backend.src.access_service.application.dto import UserIdRequest
from backend.src.access_service.application.graphic_request import GraphicRequest


@pytest.mark.asyncio
async def test_graphic_request_no_messages():
    chat_gateway = AsyncMock()
    user_gateway = AsyncMock()
    user_gateway.get_user_by_id.return_value = MagicMock()
    uow = AsyncMock()

    chat_gateway.get_all_messages.return_value = []

    service = GraphicRequest(chat_gateway, user_gateway, uow)
    result = await service.execute(UserIdRequest(user_id=1))

    assert result == "Нет сообщений за последние 30 дней"

