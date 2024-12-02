from pydantic import BaseModel
from typing import List, Optional

class Hourly(BaseModel):
    time: List[str]
    temperature_2m: Optional[List[float]] = None
    rain: Optional[List[float]] = None


class Data(BaseModel):
    donnee: Hourly