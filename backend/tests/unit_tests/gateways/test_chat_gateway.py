import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime

from backend.src.access_service.adapters.gateways.chat_gateway import ChatGatewayImpl
from backend.src.access_service.models.chat import Chat
from backend.src.access_service.models.message import Message


@pytest.mark.asyncio
async def test_get_chat_by_uuid_returns_chat():
    session = AsyncMock()
    gateway = ChatGatewayImpl(session=session)

    chat = Chat(chat_id=uuid4(), created_at=datetime.now())
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = chat
    session.execute.return_value = result_mock

    result = await gateway.get_chat_by_uuid(chat.chat_id)

    assert result == chat
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_messages_returns_list_of_dicts():
    session = AsyncMock()
    gateway = ChatGatewayImpl(session=session)

    now = datetime.now()
    messages = [
        Message(
            message_id=uuid4(),
            user_id=1,
            content="hello",
            ai_response="hi",
            created_at=now,
            chat_id=uuid4()
        )
    ]

    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = messages
    session.execute.return_value = result_mock

    result = await gateway.get_all_messages(user_id=1)

    assert isinstance(result, list)
    assert result[0]["content"] == "hello"
    session.execute.assert_awaited_once()
