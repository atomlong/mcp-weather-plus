from typing import Any, Dict, List
from mcp.server import Server
from mcp.types import Tool, TextContent, EmbeddedResource, ImageContent
import mcp.types as types
from mcp_weather_plus.tools.toolhandler import ToolHandler
from mcp_weather_plus.services.air_quality import AirQualityService
from mcp_weather_plus.services.weather import WeatherService
from mcp_weather_plus.exceptions import InvalidParameterError

class AirQualityTools(ToolHandler):
    def __init__(self):
        self.aq_service = AirQualityService()
        self.weather_service = WeatherService() # Needed for Geocoding

    def get_tools(self) -> List[types.Tool]:
        return [
            types.Tool(
                name="get_air_quality",
                description="Get current air quality metrics for a city.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "City name (e.g. 'London')"},
                    },
                    "required": ["city"],
                },
            ),
            types.Tool(
                name="get_air_quality_details",
                description="Get detailed raw air quality data (JSON) for a city.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "City name (e.g. 'London')"},
                    },
                    "required": ["city"],
                },
            ),
        ]

    async def handle_call(self, name: str, args: Dict[str, Any]) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name == "get_air_quality":
            city = args.get("city")
            if not city:
                raise InvalidParameterError("Missing 'city' parameter")
            
            coords = await self.weather_service.get_coordinates(city)
            aq_data = await self.aq_service.get_air_quality(coords.latitude, coords.longitude)
            return [types.TextContent(type="text", text=aq_data.to_markdown())]

        elif name == "get_air_quality_details":
            city = args.get("city")
            if not city:
                raise InvalidParameterError("Missing 'city' parameter")

            coords = await self.weather_service.get_coordinates(city)
            data = await self.aq_service.get_air_quality_details(coords.latitude, coords.longitude)
            
            # Return as JSON string
            import json
            return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

        raise ValueError(f"Unknown tool: {name}")
