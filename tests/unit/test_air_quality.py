import pytest
import respx
from httpx import Response
from weather_mcp.services.air_quality import AirQualityService

@pytest.mark.asyncio
async def test_get_air_quality(respx_mock):
    respx_mock.get("https://air-quality-api.open-meteo.com/v1/air-quality").mock(
        return_value=Response(200, json={
            "current": {
                "us_aqi": 25,
                "pm10": 10.0,
                "pm2_5": 5.0,
                "ozone": 60.0,
                "carbon_monoxide": 200.0,
                "nitrogen_dioxide": 10.0,
                "sulphur_dioxide": 2.0
            }
        })
    )
    
    service = AirQualityService()
    aq = await service.get_air_quality(51.5074, -0.1278)
    assert aq.aqi == 25
    assert aq.pm2_5 == 5.0
    assert aq.get_aqi_level() == "Good"

@pytest.mark.asyncio
async def test_get_air_quality_details(respx_mock):
    respx_mock.get("https://air-quality-api.open-meteo.com/v1/air-quality").mock(
        return_value=Response(200, json={
            "current": {
                "us_aqi": 25,
                "pm10": 10.0
            },
            "hourly": {
                "us_aqi": [20, 25, 30]
            }
        })
    )
    
    service = AirQualityService()
    details = await service.get_air_quality_details(51.5074, -0.1278)
    assert details["current"]["us_aqi"] == 25
    assert details["hourly"]["us_aqi"] == [20, 25, 30]
