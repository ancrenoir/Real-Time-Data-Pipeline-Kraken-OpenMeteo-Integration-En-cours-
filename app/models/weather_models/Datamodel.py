from pydantic import BaseModel
from typing import List, Optional

class Hourly(BaseModel):
    time: List[str]
    temperature_2m: List[float]
    rain: List[float]
    uv_index: Optional[List[float]]
    cloud_cover: Optional[list[float]]
    pression_surface: Optional[list[float]]
    wind_speed_80m: Optional[list[float]]
    wind_direction_10m: Optional[list[float]]
    soil_temperature_0cm: Optional[list[float]]
    soil_temperature_18cm: Optional[list[float]]
    soil_temperature_54cm: Optional[list[float]]

class Datadaily(BaseModel):
    time: List[str]
    temperature_2m_max: Optional[List[float]]
    temperature_2m_min: Optional[List[float]]
    daylight_duration: Optional[list[float]]
    sunshine_duration: Optional[list[float]]
    uv_index_max: Optional[list[float]]
    precipitation_sum: Optional[list[float]]
    rain_sum: Optional[list[float]]
    precipitation_hours: Optional[list[float]]
    wind_speed_10m_max: Optional[list[float]]
    wind_gusts_10m_max: Optional[list[float]]



class Data(BaseModel):
    donnee: Hourly

class Data_daily(BaseModel):
    données: Datadaily