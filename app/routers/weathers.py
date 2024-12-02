from fastapi import APIRouter, HTTPException
from app.services.weather_service import get_weather_data

router = APIRouter()

@router.get("/{latitude}/{longitude}")
async def weather_data(latitude: float, longitude: float):
    data = get_weather_data(latitude, longitude)
    return data
    #if 'error' in data:
        #raise HTTPException(status_code=404, detail=data['error'])
