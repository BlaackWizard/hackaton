from dishka import make_async_container
from .providers.adapters import adapter_provider
from .providers.gateways import GatewayProvider
from .providers.config import ConfigProvider
from .providers.interactors import InteractorProvider

def get_container():

    return make_async_container(
        adapter_provider(),
        ConfigProvider(),
        InteractorProvider(),
        GatewayProvider()
    )
