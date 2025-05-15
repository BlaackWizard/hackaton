import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock

from backend.src.access_service.application.dto import UserIdRequest
from backend.src.access_service.application.frequent_requests import FrequentRequests


@pytest.mark.asyncio
async def test_frequent_requests_with_recent_messages():
    chat_gateway = AsyncMock()
    ai_model = AsyncMock()
    now = datetime.now()

    chat_gateway.get_all_messages.return_value = [
        {"created_at": (now - timedelta(days=1)).isoformat(), "content": "hi"}
    ]
    ai_model.generate_text.return_value = "Summary"

    service = FrequentRequests(chat_gateway, ai_model)
    result = await service.execute(UserIdRequest(user_id=1))

    assert result == {"summary": "Summary"}


@pytest.mark.asyncio
async def test_frequent_requests_no_recent_messages():
    chat_gateway = AsyncMock()
    ai_model = AsyncMock()
    old_date = (datetime.now() - timedelta(days=60)).isoformat()
    chat_gateway.get_all_messages.return_value = [{"created_at": old_date}]

    service = FrequentRequests(chat_gateway, ai_model)
    result = await service.execute(UserIdRequest(user_id=1))

    assert result == {"summary": "Нет сообщений за последние 30 дней."}
