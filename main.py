from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, HTTPException, Query, Depends

from core.container import Container
from services.exchange_rate import ExchangeRateService

app = FastAPI()
container = Container()


@app.get('/api/rates', response_model=None)
@inject
async def get_exchange_rate(
    from_currency: str = Query(..., description="The currency code to convert from"),
    to_currency: str = Query(..., description="The currency code to convert to"),
    value: float = Query(1.0, description="The amount of currency to convert"),
    exchange_rate_service: ExchangeRateService = Depends(
        Provide[Container.exchange_rate_service]
    ),
):
    try:
        exchange_rate: float | None = await exchange_rate_service.get_cached_rate(
            from_currency,
            to_currency,
        )

        if not exchange_rate:
            exchange_rate: float = await exchange_rate_service.fetch_exchange_rate(
                from_currency,
                to_currency
            )

        converted_amount: float = await exchange_rate_service.convert_currency(
            exchange_rate,
            value
        )

        return {
            'result': round(converted_amount, 2),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


container.wire(modules=[__name__])
