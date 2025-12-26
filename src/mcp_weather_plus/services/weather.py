from typing import Any, Dict, List, Optional
import httpx
from mcp_weather_plus.utils import get_http_client
from mcp_weather_plus.exceptions import ApiError, GeocodingError
from mcp_weather_plus.models import Coordinates, WeatherForecast

class WeatherService:
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    async def get_coordinates(self, city: str) -> Coordinates:
        client = get_http_client()
        try:
            response = await client.get(self.GEOCODING_URL, params={"name": city, "count": 1, "language": "en", "format": "json"})
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as e:
            raise ApiError(f"Geocoding API failed: {str(e)}") from e

        if not data.get("results"):
            raise GeocodingError(f"City not found: {city}")

        result = data["results"][0]
        return Coordinates(latitude=result["latitude"], longitude=result["longitude"])

    async def get_current_weather(self, lat: float, lon: float) -> WeatherForecast:
        client = get_http_client()
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "weather_code", "wind_speed_10m", "wind_direction_10m", "visibility"],
            "daily": ["uv_index_max"],
            "timezone": "auto"
        }
        
        try:
            response = await client.get(self.WEATHER_URL, params=params)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as e:
            raise ApiError(f"Weather API failed: {str(e)}") from e

        current = data["current"]
        daily = data.get("daily", {})
        
        return WeatherForecast(
            temperature=current["temperature_2m"],
            feels_like=current["apparent_temperature"],
            humidity=current["relative_humidity_2m"],
            wind_speed=current["wind_speed_10m"],
            wind_direction=current["wind_direction_10m"],
            precipitation=current["precipitation"],
            uv_index=daily.get("uv_index_max", [0])[0] if daily.get("uv_index_max") else 0.0,
            visibility=current.get("visibility", 0)
        )

    async def get_weather_details(self, lat: float, lon: float) -> Dict[str, Any]:
        client = get_http_client()
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "visibility"],
            "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation_probability", "precipitation", "weather_code", "pressure_msl", "surface_pressure", "cloud_cover", "visibility", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "uv_index"],
            "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "uv_index_max", "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_hours", "precipitation_probability_max"],
            "timezone": "auto"
        }
        
        try:
            response = await client.get(self.WEATHER_URL, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise ApiError(f"Weather API failed: {str(e)}") from e

    async def get_weather_by_range(self, lat: float, lon: float, start_date: str, end_date: str) -> Dict[str, Any]:
        client = get_http_client()
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ["temperature_2m", "precipitation_probability", "wind_speed_10m"],
            "timezone": "auto"
        }
        
        try:
            response = await client.get(self.WEATHER_URL, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise ApiError(f"Weather API failed: {str(e)}") from e
