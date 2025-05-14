from backend.src.application.common.gateways.user_gateway import UserGateway
from backend.src.application.common.gateways.chat_gateway import ChatGateway
from backend.src.application.common.gateways.message_gateway import MessageGateway

from backend.src.adapters.gateways.chat_gateway import ChatGatewayImpl
from backend.src.adapters.gateways.message_gateway import MessageGatewayImpl
from backend.src.adapters.gateways.user_gateway import UserGatewayImpl

from dishka import Provider, Scope, provide

class GatewayProvider(Provider):
    scope = Scope.REQUEST

    chat_gateway = provide(ChatGatewayImpl, provides=ChatGateway)
    user_gateway = provide(UserGatewayImpl, provides=UserGateway)
    message_gateway = provide(MessageGatewayImpl, provides=MessageGateway)
