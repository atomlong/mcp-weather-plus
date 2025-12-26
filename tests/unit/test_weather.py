import pytest
import respx
from httpx import Response
from weather_mcp.services.weather import WeatherService
from weather_mcp.exceptions import GeocodingError

@pytest.mark.asyncio
async def test_get_coordinates_success(respx_mock):
    respx_mock.get("https://geocoding-api.open-meteo.com/v1/search").mock(
        return_value=Response(200, json={"results": [{"latitude": 51.5074, "longitude": -0.1278}]})
    )
    
    service = WeatherService()
    coords = await service.get_coordinates("London")
    assert coords.latitude == 51.5074
    assert coords.longitude == -0.1278

@pytest.mark.asyncio
async def test_get_coordinates_not_found(respx_mock):
    respx_mock.get("https://geocoding-api.open-meteo.com/v1/search").mock(
        return_value=Response(200, json={"results": []})
    )
    
    service = WeatherService()
    with pytest.raises(GeocodingError):
        await service.get_coordinates("NonExistentCity")

@pytest.mark.asyncio
async def test_get_current_weather(respx_mock):
    respx_mock.get("https://api.open-meteo.com/v1/forecast").mock(
        return_value=Response(200, json={
            "current": {
                "temperature_2m": 20.0,
                "apparent_temperature": 19.5,
                "relative_humidity_2m": 50,
                "wind_speed_10m": 10.0,
                "wind_direction_10m": 180,
                "precipitation": 0.0,
                "visibility": 10000.0,
                "weather_code": 0
            },
            "daily": {
                "uv_index_max": [5.0]
            }
        })
    )
    
    service = WeatherService()
    forecast = await service.get_current_weather(51.5074, -0.1278)
    assert forecast.temperature == 20.0
    assert forecast.uv_index == 5.0
