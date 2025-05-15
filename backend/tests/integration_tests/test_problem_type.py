import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock

from backend.src.access_service.application.dto import UserIdRequest
from backend.src.access_service.application.problem_type import ProblemType


@pytest.mark.asyncio
async def test_problem_type_with_data():
    chat_gateway = AsyncMock()
    ai_model = AsyncMock()
    now = datetime.now()

    messages = [
        {"created_at": (now - timedelta(days=2)).isoformat(), "content": "problem A"},
        {"created_at": (now - timedelta(days=1)).isoformat(), "content": "problem B"},
    ]

    chat_gateway.get_all_messages.return_value = messages
    ai_model.generate_text.return_value = "Категория: 2"

    service = ProblemType(chat_gateway, ai_model)
    result = await service.execute(UserIdRequest(user_id=1))

    assert "Категория" in result["categories"]


@pytest.mark.asyncio
async def test_problem_type_no_recent_messages():
    chat_gateway = AsyncMock()
    ai_model = AsyncMock()
    old_date = (datetime.now() - timedelta(days=60)).isoformat()
    chat_gateway.get_all_messages.return_value = [{"created_at": old_date}]

    service = ProblemType(chat_gateway, ai_model)
    result = await service.execute(UserIdRequest(user_id=1))

    assert result == {"categories": "Нет сообщений за последние 30 дней."}
