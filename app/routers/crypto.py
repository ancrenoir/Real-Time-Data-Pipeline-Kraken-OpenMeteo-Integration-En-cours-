from fastapi import APIRouter, HTTPException
from app.services.crypto_service import get_crypto_pair_data
# from app.services.kafka_sercice import produce_to_kafka

router = APIRouter()

@router.get("/{symbol}")
async def crypto_data(symbol: str):
    data = get_crypto_pair_data(symbol)
    if isinstance(data, list) and "error" and "invalid" in data:
        raise HTTPException(status_code=404, detail = "erreur dans la tantative de "
                                                      "recuperation de la donnée")
    return data


