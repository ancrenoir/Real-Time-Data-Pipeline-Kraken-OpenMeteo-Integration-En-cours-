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

class data_asks_bids_endpoint(BaseModel):
    Data_endpoint_order_book: data_asks_bids

'''
   Les models pour la endpoint recent trades de l'API de kraken
'''
## cette classe va créer un objet qui va contenir les données
class recent_trades_object(BaseModel):
    couple_crypto:str
    Price: List[str]
    volume: List[str]
    temps: List[float]
    order_type: List[str]
    market_limit: List[str]
    miscellaneous: List[str]
    trade_id: List[int]

## cette classe va créer un objet qui va contenir l'objet qui contient nos données et le nom des couples de crypto
class recent_trades_crypto_final(BaseModel):
    Data_endpoint_recent_trades: recent_trades_object