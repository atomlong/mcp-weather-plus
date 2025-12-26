from typing import Any, Dict, List
from mcp.server import Server
from mcp.types import Tool, TextContent, EmbeddedResource, ImageContent
import mcp.types as types
from mcp_weather_plus.tools.toolhandler import ToolHandler
from mcp_weather_plus.services.time import TimeService
from mcp_weather_plus.exceptions import InvalidParameterError

class TimeTools(ToolHandler):
    def __init__(self):
        self.time_service = TimeService()

    def get_tools(self) -> List[types.Tool]:
        return [
            types.Tool(
                name="get_current_datetime",
                description="Get current datetime for a specific timezone.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "timezone_name": {"type": "string", "description": "IANA Timezone name (e.g. 'Asia/Shanghai')"},
                    },
                    "required": ["timezone_name"],
                },
            ),
            types.Tool(
                name="get_timezone_info",
                description="Get information about a specific timezone.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "timezone_name": {"type": "string", "description": "IANA Timezone name (e.g. 'Asia/Shanghai')"},
                    },
                    "required": ["timezone_name"],
                },
            ),
            types.Tool(
                name="convert_time",
                description="Convert time between timezones.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "time_str": {"type": "string", "description": "Time string in ISO format"},
                        "from_timezone": {"type": "string", "description": "Source timezone name"},
                        "to_timezone": {"type": "string", "description": "Target timezone name"},
                    },
                    "required": ["time_str", "from_timezone", "to_timezone"],
                },
            ),
        ]

    async def handle_call(self, name: str, args: Dict[str, Any]) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name == "get_current_datetime":
            timezone_name = args.get("timezone_name")
            if not timezone_name:
                raise InvalidParameterError("Missing 'timezone_name' parameter")
            
            result = self.time_service.get_current_datetime(timezone_name)
            return [types.TextContent(type="text", text=result)]

        elif name == "get_timezone_info":
            timezone_name = args.get("timezone_name")
            if not timezone_name:
                raise InvalidParameterError("Missing 'timezone_name' parameter")

            result = self.time_service.get_timezone_info(timezone_name)
            import json
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "convert_time":
            time_str = args.get("time_str")
            from_timezone = args.get("from_timezone")
            to_timezone = args.get("to_timezone")
            
            if not all([time_str, from_timezone, to_timezone]):
                raise InvalidParameterError("Missing required parameters: time_str, from_timezone, to_timezone")

            result = self.time_service.convert_time(time_str, from_timezone, to_timezone)
            return [types.TextContent(type="text", text=result)]

        raise ValueError(f"Unknown tool: {name}")
