# services/weather_service.py

import requests
from config import WEATHER_API_KEY, CITY_NAME

class WeatherService:
    def __init__(self, api_key, city_name):
        self.api_key = api_key
        self.city_name = city_name
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

    def get_weather(self):
        params = {
            'q': self.city_name,
            'appid': self.api_key,
            'units': 'metric',  # Используем метрическую систему для отображения температуры в градусах Цельсия
            'lang': 'ru'  # Устанавливаем язык на русский
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
