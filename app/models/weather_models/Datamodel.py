from pydantic import BaseModel
from typing import List, Optional

class Hourly(BaseModel):
    time: List[str]
    temperature_2m: List[float]
    rain: List[float]


class Data(BaseModel):
    donnee: Hourly