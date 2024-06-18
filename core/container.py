import aioredis

from dependency_injector import containers, providers

from core.config import Settings
from services.exchange_rate import ExchangeRateService


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(Settings)

    redis = providers.Singleton(
        aioredis.from_url,
        "redis://redis:6379",
        encoding="utf-8",
        decode_responses=True
    )

    exchange_rate_service = providers.Singleton(ExchangeRateService, redis)
