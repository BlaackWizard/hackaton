import pytest
from unittest.mock import AsyncMock

from backend.src.access_service.application.dto import UserIdRequest
from backend.src.access_service.application.history import History


@pytest.mark.asyncio
async def test_history_returns_messages():
    chat_gateway = AsyncMock()
    messages = [{"content": "msg1"}]
    chat_gateway.get_all_messages.return_value = messages

    service = History(chat_gateway)
    result = await service.execute(UserIdRequest(user_id=1))

    assert result == messages
