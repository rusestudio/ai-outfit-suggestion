import requests
import os

GOOGLE_WEATHER_API_KEY = os.getenv("API_KEY_WEATHER")

def get_weather(latitude: float, longitude: float):
    """
    TEMP implementation using Open-Meteo style response.
    Replace URL later with Google-backed service if needed.
    """

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    current = data.get("current", {})

    return {
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "rain": current.get("precipitation"),
        "wind": current.get("wind_speed_10m"),
    }
