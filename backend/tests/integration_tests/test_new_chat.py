import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.src.access_service.application.dto import UserIdRequest
from backend.src.access_service.application.exceptions.user import NotFoundUserError
from backend.src.access_service.application.new_chat import NewChat


@pytest.mark.asyncio
async def test_new_chat_success():
    uow = AsyncMock()
    user_gateway = AsyncMock()
    chat_gateway = AsyncMock()

    user = MagicMock()
    user_gateway.get_user_by_id.return_value = user

    service = NewChat(chat_gateway, user_gateway, uow)
    await service.execute(UserIdRequest(user_id=1))

    uow.add.assert_any_call(user)
    uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_new_chat_user_not_found():
    uow = AsyncMock()
    user_gateway = AsyncMock()
    chat_gateway = AsyncMock()
    user_gateway.get_user_by_id.return_value = None

    service = NewChat(chat_gateway, user_gateway, uow)

    with pytest.raises(NotFoundUserError):
        await service.execute(UserIdRequest(user_id=1))
