import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.src.access_service.adapters.gateways.user_gateway import UserGatewayImpl
from backend.src.access_service.models.user import User

@pytest.mark.asyncio
async def test_get_user_by_id_returns_user():
    session = AsyncMock()
    gateway = UserGatewayImpl(session=session)

    user = User(user_id=1, chat_id=None)

    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = user
    session.execute.return_value = result_mock

    result = await gateway.get_user_by_id(1)

    assert result == user
    session.execute.assert_awaited_once()
