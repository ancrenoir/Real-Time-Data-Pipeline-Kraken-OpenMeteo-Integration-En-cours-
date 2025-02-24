import requests
from decouple import config
import requests_cache
from retry_requests import retry
import openmeteo_requests
from app.models.weather_models.Datamodel import Hourly, Data, Datadaily, Data_daily
import pandas as pd
'''
Définition de la fonction get_weather_data pour les endpoints par heurs, les hourly data
'''
# Configuration de l'URL de l'API météo
WEATHER_URL = config('URL_WEATHER', default="https://api.open-meteo.com/v1/forecast")

# Initialisation de la session de cache et de la session de retry
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

# Initialisation du client Open-Meteo
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_weather_data_hourly(latitude: float, longitude: float, openmeteo=openmeteo) -> Data:
    # Paramètres pour la requête API
    hourly_params = ["temperature_2m", "rain", "uv_index", "cloud_cover", "surface_pressure",
                     "wind_speed_80m", "wind_direction_10m", "soil_temperature_0cm",
                     "soil_temperature_18cm", "soil_temperature_54cm"]
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
        ).astype(str).to_list()

        # Remplir le dictionnaire de données
        for i in range(hourly_object.VariablesLength()):
            data[hourly_params[i]] = hourly_object.Variables(i).ValuesAsNumpy().tolist()

        # Créer l'objet Hourly
        hourly = Hourly(
            time=time,
            temperature_2m=data["temperature_2m"],
            rain=data["rain"],
            uv_index=data["uv_index"],
            cloud_cover=data["cloud_cover"],
            pression_surface=data["surface_pressure"],
            wind_speed_80m=data["wind_speed_80m"],
            wind_direction_10m=data["wind_direction_10m"],
            soil_temperature_0cm=data["soil_temperature_0cm"],
            soil_temperature_18cm=data["soil_temperature_18cm"],
            soil_temperature_54cm=data["soil_temperature_54cm"]

         )
        instance_Data= Data(
        donnee=hourly
        )

       # Retourner l'objet Data
        return instance_Data.dict()
    except requests.exceptions.RequestException as e:
        print(f"l'exception lévé: {e}")

'''
Définition de la fonction get_weather_data_daily
'''
def get_weather_data_daily(latitude: float, longitude: float, openmeteo=openmeteo) -> Data_daily:

    '''Température maximale à 2 mètres (°C)
    Température minimale à 2 mètres (°C)
    Durée de la lumière du jour (heures)
    Durée d'ensoleillement direct (heures)
    Indice UV maximal (sans unité)
    Somme des précipitations (mm)
    Quantité de pluie uniquement (mm)
    Quantité de neige (cm)
    Probabilité maximale de précipitations (%)
    Vitesse maximale du vent à 10 mètres (km/h)
    Rafales de vent maximales à 10 mètres (km/h)  '''

    daily_params = ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset",
                    "daylight_duration", "sunshine_duration", "uv_index_max", "precipitation_sum",
                    "rain_sum", "precipitation_hours", "wind_speed_10m_max", "wind_gusts_10m_max"]
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join(daily_params)
    }

    try:
        ''' Récuperation de l'objet retourné par l'api d'openméteo, et iteration sur l'objet 
            pour interagir avec les données jounalière récupérées '''

        reponses= openmeteo.weather_api(WEATHER_URL, params=params)
        data_object= reponses[0]
        daily_object= data_object.Daily()



        ## générer une plage de temps au format iso pour récuperer la donnée time

        time = pd.date_range(
            start= pd.to_datetime(daily_object.Time(), unit= "s", utc=True),
            end= pd.to_datetime(daily_object.TimeEnd(), unit= "s", utc=True),
            freq= pd.Timedelta(seconds= daily_object.Interval()),
            inclusive= "left").astype(str).to_list()

        # Initialisation d'un dictionnaire en comprehension pour récuperer chaque donnnée et de les formaté en liste
        data= {
            f"{daily_params[i]}": daily_object.Variables(i).ValuesAsNumpy()
            for i in range(daily_object.VariablesLength())
        }

        # Création d'intance de classes Datadaily et data pour la validation de schema et un format accepté par API d'openmetéo

        intance_data_daily= Datadaily(
            time= time,
            temperature_2m_max= data["temperature_2m_max"].tolist(),
            temperature_2m_min= data["temperature_2m_min"].tolist(),
            daylight_duration= data["daylight_duration"].tolist(),
            sunshine_duration= data["sunshine_duration"].tolist(),
            uv_index_max= data["uv_index_max"].tolist(),
            precipitation_sum= data["precipitation_sum"].tolist(),
            rain_sum= data["rain_sum"].tolist(),
            precipitation_hours= data["precipitation_hours"].tolist(),
            wind_speed_10m_max= data["wind_speed_10m_max"].tolist(),
            wind_gusts_10m_max= data["wind_gusts_10m_max"].tolist()
        )

        instance_data= Data_daily(
            données= intance_data_daily
        )

        return instance_data.dict()

    except requests.exceptions.RequestException as e:
        print(f"l'exception lévé est: {e}")
