import requests
import aioredis

from fastapi import FastAPI, HTTPException, Query

from core.config import settings

app = FastAPI()

redis = aioredis.from_url("redis://redis:6379", encoding="utf-8", decode_responses=True)


@app.get('/api/rates')
async def get_exchange_rate(
        from_currency: str = Query(..., description="The currency code to convert from"),
        to_currency: str = Query(..., description="The currency code to convert to"),
        value: float = Query(1.0, description="The amount of currency to convert")
):
    try:
        cache_key = f"{from_currency}_{to_currency}"
        cached_rate = await redis.get(cache_key)
        is_from_cache = False

        if cached_rate:
            exchange_rate = float(cached_rate)
            is_from_cache = True
        else:
            response = requests.get(f'{settings.exchange_rate_url}/{from_currency}')
            data = response.json()

            if data['result'] != 'success':
                raise HTTPException(status_code=500, detail="Error fetching exchange rate.")

            exchange_rate = data['conversion_rates'].get(to_currency)
            if exchange_rate is None:
                raise HTTPException(status_code=400, detail=f"Unsupported currency code: {to_currency}")

            await redis.set(cache_key, exchange_rate, ex=30)

        converted_amount = exchange_rate * value
        return {
            'result': round(converted_amount, 2),
            'is_from_cache': is_from_cache,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/api/put')
async def put_into_redis(
        from_currency: str = Query(..., description="The currency code to convert from"),
        to_currency: str = Query(..., description="The currency code to convert to"),
):
    cache_key = f"{from_currency}_{to_currency}"
    exchange_rate = 90
    await redis.set(cache_key, exchange_rate, ex=300)


@app.get('/api/get')
async def put_into_redis(
        from_currency: str = Query(..., description="The currency code to convert from"),
        to_currency: str = Query(..., description="The currency code to convert to"),
):
    cache_key = f"{from_currency}_{to_currency}"
    cached_rate = await redis.get(cache_key)
    return {'cached_rate': cached_rate}
