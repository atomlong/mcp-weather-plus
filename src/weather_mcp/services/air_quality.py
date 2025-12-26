from typing import Any, Dict, List, Optional
import httpx
from weather_mcp.utils import get_http_client
from weather_mcp.exceptions import ApiError
from weather_mcp.models import AirQualityData

class AirQualityService:
    AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

    async def get_air_quality(self, lat: float, lon: float) -> AirQualityData:
        client = get_http_client()
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["us_aqi", "pm10", "pm2_5", "ozone", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide"],
            "timezone": "auto"
        }
        
        try:
            response = await client.get(self.AIR_QUALITY_URL, params=params)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as e:
            raise ApiError(f"Air Quality API failed: {str(e)}") from e

        current = data["current"]
        
        return AirQualityData(
            aqi=current["us_aqi"],
            pm2_5=current["pm2_5"],
            pm10=current["pm10"],
            ozone=current["ozone"],
            carbon_monoxide=current["carbon_monoxide"],
            nitrogen_dioxide=current["nitrogen_dioxide"],
            sulphur_dioxide=current["sulphur_dioxide"]
        )

    async def get_air_quality_details(self, lat: float, lon: float) -> Dict[str, Any]:
        client = get_http_client()
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["us_aqi", "pm10", "pm2_5", "ozone", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide", "european_aqi"],
            "hourly": ["pm10", "pm2_5", "ozone", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide", "us_aqi", "european_aqi"],
            "timezone": "auto"
        }
        
        try:
            response = await client.get(self.AIR_QUALITY_URL, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise ApiError(f"Air Quality API failed: {str(e)}") from e
