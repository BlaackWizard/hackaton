from pathlib import Path

from backend.src.access_service.adapters.config_loader import DBConfig, AIModelConfig
from dishka import Provider, provide, Scope, provide_all

class ConfigProvider(Provider):
    scope = Scope.APP

    provides = provide_all(
        AIModelConfig, DBConfig
    )

