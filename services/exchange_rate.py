import requests
from fastapi import HTTPException
from core.config import settings


class ExchangeRateService:
    def __init__(self, redis):
        self.redis = redis

    async def cache_exchange_rate(
        self,
        from_currency: str,
        to_currency: str,
        rate: float,
        ttl: int = 300
    ):
        cache_key = f"{from_currency}_{to_currency}"
        await self.redis.set(cache_key, rate, ex=ttl)

    async def get_cached_rate(
        self,
        from_currency: str,
        to_currency: str
    ) -> float | None:
        cache_key = f"{from_currency}_{to_currency}"
        cached_rate = await self.redis.get(cache_key)
        if cached_rate:
            return float(cached_rate)

    @staticmethod
    async def fetch_exchange_rate(
        from_currency: str,
        to_currency: str
    ) -> float:
        response = requests.get(f'{settings.exchange_rate_url}/{from_currency}')
        data = response.json()

        if data['result'] != 'success':
            raise HTTPException(status_code=500, detail="Error fetching exchange rate.")

        exchange_rate = data['conversion_rates'].get(to_currency)
        if exchange_rate is None:
            raise HTTPException(status_code=400, detail=f"Unsupported currency code: {to_currency}")

        return exchange_rate

    @staticmethod
    async def convert_currency(
        exchange_rate: float,
        value: float
    ) -> float:
        return exchange_rate * value
