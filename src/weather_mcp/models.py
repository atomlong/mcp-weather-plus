from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class Coordinates(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude of the location")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude of the location")

class WeatherForecast(BaseModel):
    temperature: float = Field(..., description="Temperature in Celsius")
    feels_like: float = Field(..., description="Apparent temperature in Celsius")
    humidity: int = Field(..., description="Relative humidity in percent")
    wind_speed: float = Field(..., description="Wind speed in km/h")
    wind_direction: int = Field(..., description="Wind direction in degrees")
    precipitation: float = Field(..., description="Precipitation in mm")
    uv_index: float = Field(..., description="UV Index")
    visibility: float = Field(..., description="Visibility in meters")

    def to_markdown(self) -> str:
        return f"""
### Current Weather
- **Temperature**: {self.temperature}°C
- **Feels Like**: {self.feels_like}°C
- **Humidity**: {self.humidity}%
- **Wind**: {self.wind_speed} km/h (Direction: {self.wind_direction}°)
- **Precipitation**: {self.precipitation} mm
- **UV Index**: {self.uv_index}
- **Visibility**: {self.visibility} m
"""

class AirQualityData(BaseModel):
    aqi: int = Field(..., description="Air Quality Index")
    pm2_5: float = Field(..., description="PM2.5 concentration")
    pm10: float = Field(..., description="PM10 concentration")
    ozone: float = Field(..., description="Ozone concentration")
    carbon_monoxide: Optional[float] = Field(None, description="Carbon Monoxide concentration")
    nitrogen_dioxide: Optional[float] = Field(None, description="Nitrogen Dioxide concentration")
    sulphur_dioxide: Optional[float] = Field(None, description="Sulphur Dioxide concentration")

    def get_aqi_level(self) -> str:
        if self.aqi <= 50: return "Good"
        if self.aqi <= 100: return "Moderate"
        if self.aqi <= 150: return "Unhealthy for Sensitive Groups"
        if self.aqi <= 200: return "Unhealthy"
        if self.aqi <= 300: return "Very Unhealthy"
        return "Hazardous"

    def to_markdown(self) -> str:
        return f"""
### Air Quality
- **AQI**: {self.aqi} ({self.get_aqi_level()})
- **PM2.5**: {self.pm2_5} µg/m³
- **PM10**: {self.pm10} µg/m³
- **Ozone**: {self.ozone} µg/m³
"""
