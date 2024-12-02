from pydantic import BaseModel
from typing import List, Optional

class Data_crypto(BaseModel):
    price: List[float]
    volume: List[float]
    temps: List[int]

class data_asks_bids(BaseModel):
    couple_crypto: str
    asks: Data_crypto
    bids: Data_crypto

