import logging
from typing import Optional, Literal
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.sse import SseServerTransport
import mcp.types as types
from starlette.applications import Starlette
from starlette.routing import Route, Mount
import uvicorn

from weather_mcp.tools.weather import WeatherTools
from weather_mcp.tools.air_quality import AirQualityTools
from weather_mcp.tools.time import TimeTools
from weather_mcp.utils import close_http_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather-mcp")

def create_mcp_server() -> Server:
    server = Server("weather-mcp")
    
    # Register tool handlers
    weather_tools = WeatherTools()
    aq_tools = AirQualityTools()
    time_tools = TimeTools()
    
    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return (
            weather_tools.get_tools() +
            aq_tools.get_tools() +
            time_tools.get_tools()
        )

    # Register tool execution handler
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict):
        if name in ["get_current_weather", "get_weather_by_datetime_range", "get_weather_details"]:
            return await weather_tools.handle_call(name, arguments)
        elif name in ["get_air_quality", "get_air_quality_details"]:
            return await aq_tools.handle_call(name, arguments)
        elif name in ["get_current_datetime", "get_timezone_info", "convert_time"]:
            return await time_tools.handle_call(name, arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

    return server

async def run_stdio_server():
    server = create_mcp_server()
    async with stdio_server() as (read_stream, write_stream):
        try:
            await server.run(read_stream, write_stream, server.create_initialization_options())
        finally:
            await close_http_client()

async def run_http_server(port: int = 8080):
    server = create_mcp_server()
    sse = SseServerTransport("/messages")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await server.run(
                streams[0], streams[1], server.create_initialization_options()
            )

    async def handle_messages(request):
        await sse.handle_post_message(request.scope, request.receive, request._send)

    app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Route("/messages", endpoint=handle_messages, methods=["POST"]),
        ],
    )

    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server_instance = uvicorn.Server(config)
    
    try:
        await server_instance.serve()
    finally:
        await close_http_client()

def serve(mode: Literal["stdio", "streamable-http"] = "stdio", port: int = 8080):
    import asyncio
    if mode == "stdio":
        asyncio.run(run_stdio_server())
    elif mode == "streamable-http":
        asyncio.run(run_http_server(port))
    else:
        raise ValueError(f"Unknown mode: {mode}")
