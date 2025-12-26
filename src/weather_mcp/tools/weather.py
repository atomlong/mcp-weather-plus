from typing import Any, Dict, List
from mcp.server import Server
from mcp.types import Tool, TextContent, EmbeddedResource, ImageContent
import mcp.types as types
from weather_mcp.tools.toolhandler import ToolHandler
from weather_mcp.services.weather import WeatherService
from weather_mcp.exceptions import InvalidParameterError

class WeatherTools(ToolHandler):
    def __init__(self):
        self.weather_service = WeatherService()

    def get_tools(self) -> List[types.Tool]:
        return [
            types.Tool(
                name="get_current_weather",
                description="Get current weather metrics for a city.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "City name (e.g. 'London')"},
                    },
                    "required": ["city"],
                },
            ),
            types.Tool(
                name="get_weather_by_datetime_range",
                description="Get hourly weather trends for a date range.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "City name (e.g. 'London')"},
                        "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                        "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
                    },
                    "required": ["city", "start_date", "end_date"],
                },
            ),
            types.Tool(
                name="get_weather_details",
                description="Get detailed raw weather data (JSON) for a city.",
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
        if name == "get_current_weather":
            city = args.get("city")
            if not city:
                raise InvalidParameterError("Missing 'city' parameter")
            
            coords = await self.weather_service.get_coordinates(city)
            forecast = await self.weather_service.get_current_weather(coords.latitude, coords.longitude)
            return [types.TextContent(type="text", text=forecast.to_markdown())]

        elif name == "get_weather_by_datetime_range":
            city = args.get("city")
            start_date = args.get("start_date")
            end_date = args.get("end_date")
            
            if not all([city, start_date, end_date]):
                raise InvalidParameterError("Missing required parameters: city, start_date, end_date")

            coords = await self.weather_service.get_coordinates(city)
            data = await self.weather_service.get_weather_by_range(coords.latitude, coords.longitude, start_date, end_date)
            
            # Basic formatting for now, can be improved to Markdown summary
            return [types.TextContent(type="text", text=f"Weather for {city} from {start_date} to {end_date}:\n{str(data)}")]

        elif name == "get_weather_details":
            city = args.get("city")
            if not city:
                raise InvalidParameterError("Missing 'city' parameter")

            coords = await self.weather_service.get_coordinates(city)
            data = await self.weather_service.get_weather_details(coords.latitude, coords.longitude)
            
            # Return as JSON string
            import json
            return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

        raise ValueError(f"Unknown tool: {name}")
