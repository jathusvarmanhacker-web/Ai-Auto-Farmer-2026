import requests

WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy fog", 51: "Light drizzle", 53: "Drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 80: "Light showers", 81: "Showers",
    95: "Thunderstorm",
}

FALLBACK = {
    "temp": "28°C", "temp_desc": "Partly cloudy",
    "humidity": "74%", "humidity_desc": "Optimal range",
    "rain": "30%", "rain_desc": "Light showers",
    "wind": "12 km/h", "wind_desc": "Gentle breeze",
}

def fetch_weather(location: str) -> dict:
    try:
        geo = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={requests.utils.quote(location)}&count=1",
            timeout=5,
        ).json()
        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        wd = requests.get(
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,precipitation_probability,wind_speed_10m,weather_code"
            f"&wind_speed_unit=kmh",
            timeout=5,
        ).json()
        c = wd["current"]
        hum = c["relative_humidity_2m"]
        rain = c["precipitation_probability"]
        wind = round(c["wind_speed_10m"])
        return {
            "temp": f"{round(c['temperature_2m'])}°C",
            "temp_desc": WEATHER_CODES.get(c["weather_code"], "Clear sky"),
            "humidity": f"{hum}%",
            "humidity_desc": "High humidity" if hum > 70 else "Optimal range",
            "rain": f"{rain}%",
            "rain_desc": "Expect rain" if rain > 50 else "Light showers",
            "wind": f"{wind} km/h",
            "wind_desc": "Gentle breeze" if wind < 20 else "Moderate wind",
        }
    except Exception:
        return FALLBACK
