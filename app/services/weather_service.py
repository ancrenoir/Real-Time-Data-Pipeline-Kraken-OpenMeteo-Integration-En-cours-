import requests
from decouple import config
import requests_cache
from retry_requests import retry
import openmeteo_requests
import pandas as pd
from pydantic import BaseModel
from typing import List

# Configuration de l'URL de l'API météo
WEATHER_URL = config('URL_WEATHER')

# Initialisation de la session de cache et de la session de retry
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

# Initialisation du client Open-Meteo
openmeteo = openmeteo_requests.Client(session=retry_session)

# Définition des modèles Pydantic
class Hourly(BaseModel):
    time: List[str]
    temperature_2m: List[float]
    rain: List[float]

class Data(BaseModel):
    donnee: Hourly

def get_weather_data(latitude: float, longitude: float, openmeteo=openmeteo) -> Data:
    # Paramètres pour la requête API
    hourly_params = ["temperature_2m", "rain"]
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join(hourly_params)
    }

    try:
        # Effectuer la requête API
        responses = openmeteo.weather_api(WEATHER_URL, params=params)
        # Extraire les données de la réponse
        data_object = responses[0]
        hourly_object = data_object.Hourly()

        # Initialiser le dictionnaire de données
        data = {}

        # Générer la plage de temps
        time = pd.date_range(
            start=pd.to_datetime(hourly_object.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly_object.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly_object.Interval()),
            inclusive="left"
        ).astype(str).tolist()

        # Remplir le dictionnaire de données
        for i in range(hourly_object.VariablesLength()):
            data[hourly_params[i]] = hourly_object.Variables(i).ValuesAsNumpy().tolist()

        # Créer l'objet Hourly
        hourly = Hourly(
            time=time,
            temperature_2m=data["temperature_2m"],
            rain=data["rain"]
        )

        # Créer l'objet Data
        instance_data = Data(donnee=hourly)

        # Retourner le dictionnaire de l'instance Data
        return instance_data.dict()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
