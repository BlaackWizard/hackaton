from dishka import Provider, provide, Scope
from backend.src.adapters.uow import UoWImpl
from backend.src.adapters.db.provider import get_session, get_engine, get_sessionmaker
from backend.src.adapters.ai_model import ChatGPTAiModel
from dotenv import load_dotenv
import os

from backend.src.application.common.ai_model import AiModel
from backend.src.application.common.uow import UoW


class AdapterProvider(Provider):
    scope = Scope.REQUEST

    uow = provide(UoWImpl, provides=UoW)
    ai_model = provide(ChatGPTAiModel, provides=AiModel)

def adapter_provider() -> AdapterProvider:
    provider = AdapterProvider()
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(get_session, scope=Scope.REQUEST)

    return provider
