from fastapi import APIRouter, HTTPException
from app.services.weather_service import get_weather_data_hourly, get_weather_data_daily

router = APIRouter()

@router.get("/hourly/{latitude}/{longitude}")
async def weather_data_hourly(latitude: float, longitude: float):
    data = get_weather_data_hourly(latitude, longitude)
    return data
    #if 'error' in data:
        #raise HTTPException(status_code=404, detail=data['error'])

@router.get("/daily/{latitude}/{longitude}")
async def weather_data_daily(latitude: float, longitude: float):
    data1= get_weather_data_daily(latitude, longitude)
    return data1

