import requests

from fastapi import FastAPI, HTTPException, Query

from core.config import settings

app = FastAPI()


@app.get('/api/rates')
def get_exchange_rate(
        from_currency: str = Query(..., description="The currency code to convert from"),
        to_currency: str = Query(..., description="The currency code to convert to"),
        value: float = Query(1.0, description="The amount of currency to convert")
):
    try:
        response = requests.get(f'{settings.exchange_rate_url}/{from_currency}')
        data = response.json()

        if data['result'] != 'success':
            raise HTTPException(status_code=500, detail="Error fetching exchange rate.")

        exchange_rate = data['conversion_rates'].get(to_currency)
        if exchange_rate is None:
            raise HTTPException(status_code=400, detail=f"Unsupported currency code: {to_currency}")

        converted_amount = exchange_rate * value
        return {"result": round(converted_amount, 2)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
