from fastapi import FastAPI, HTTPException, Query
from loguru import logger
import requests

app = FastAPI()

API_KEY = 'bff928288dc7fd8412f9a919'
EXCHANGE_RATE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'


@app.get('/api/rates')
def get_exchange_rate(
        from_currency: str = Query(..., description="The currency code to convert from"),
        to_currency: str = Query(..., description="The currency code to convert to"),
        value: float = Query(1.0, description="The amount of currency to convert")
):
    try:
        response = requests.get(f"{EXCHANGE_RATE_URL}{from_currency}")
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
