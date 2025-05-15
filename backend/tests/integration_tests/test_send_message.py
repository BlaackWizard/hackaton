import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

from backend.src.access_service.application.dto import NewMessageSendRequest
from backend.src.access_service.application.exceptions.user import NotFoundUserError
from backend.src.access_service.application.send_message import SendMessage


@pytest.mark.asyncio
async def test_send_message_success():
    user_gateway = AsyncMock()
    message_gateway = AsyncMock()
    uow = AsyncMock()
    ai_model = AsyncMock()

    user = MagicMock()
    user.user_id = 1
    user.chat_id = uuid4()
    user_gateway.get_user_by_id.return_value = user
    ai_model.generate_text.return_value = "AI says hi"

    service = SendMessage(message_gateway, uow, user_gateway, ai_model)
    data = NewMessageSendRequest(user_id=1, content="Hi")

    result = await service.execute(data)

    assert result == "AI says hi"
    uow.add.assert_called()
    uow.commit.assert_called()


@pytest.mark.asyncio
async def test_send_message_user_not_found():
    user_gateway = AsyncMock()
    message_gateway = AsyncMock()
    uow = AsyncMock()
    ai_model = AsyncMock()

    user_gateway.get_user_by_id.return_value = None
    service = SendMessage(message_gateway, uow, user_gateway, ai_model)

    with pytest.raises(NotFoundUserError):
        await service.execute(NewMessageSendRequest(user_id=1, content="Hi"))
