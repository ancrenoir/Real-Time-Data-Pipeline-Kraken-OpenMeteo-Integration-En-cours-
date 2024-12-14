from fastapi import APIRouter, HTTPException
from app.services.crypto_service import get_crypto_pair_data_depth, get_crypto_data_recent_trades
# from app.services.kafka_sercice import produce_to_kafka

router = APIRouter()

@router.get("/depth/{symbol}")
async def crypto_data_depth(symbol: str):
    data = get_crypto_pair_data_depth(symbol)
    if isinstance(data, list) and "error" and "invalid" in data:
        raise HTTPException(status_code=404, detail = "erreur dans la tantative de "
                                                      "recuperation de la donnée")
    return data


@router.get("/recent_trades/{symbol}")
async def crypto_data_recent_trades(symbol: str):
    data= get_crypto_data_recent_trades(symbol)
    if isinstance(data, list) and "error" and "invalid" in data:
        raise HTTPException(status_code=404, detail = "erreur dans la tantative de"
                                                      " recuperation de la données ")
    return data


