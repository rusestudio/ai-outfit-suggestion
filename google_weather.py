import requests
import os

API_KEY_WEATHER = os.getenv("API_KEY_WEATHER")

def get_weather(latitude: float, longitude: float):
    """
    Fetch current weather using OpenWeatherMap API.
    Returns temperature in Celsius, humidity %, precipitation (rain in mm), wind speed in m/s.
    """
    if not API_KEY_WEATHER:
        raise ValueError("API_KEY_WEATHER environment variable not set")

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={latitude}&lon={longitude}&appid={API_KEY_WEATHER}&units=metric"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    main = data.get("main", {})
    wind = data.get("wind", {})
    rain = data.get("rain", {}).get("1h", 0)  # precipitation in last hour, default 0

    return {
        "temperature": main.get("temp"),
        "humidity": main.get("humidity"),
        "rain": rain,
        "wind": wind.get("speed"),
    }
