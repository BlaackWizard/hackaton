import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime

from backend.src.access_service.adapters.gateways.message_gateway import MessageGatewayImpl
from backend.src.access_service.models.message import Message

@pytest.mark.asyncio
async def test_get_message_by_uuid_returns_message():
    session = AsyncMock()
    gateway = MessageGatewayImpl(session=session)

    message = Message(
        message_id=uuid4(),
        user_id=1,
        content="test",
        ai_response="response",
        created_at=datetime.now(),
        chat_id=uuid4()
    )

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = message
    session.execute.return_value = result_mock

    result = await gateway.get_message_by_uuid(message.message_id)

    assert result == message
    session.execute.assert_awaited_once()
