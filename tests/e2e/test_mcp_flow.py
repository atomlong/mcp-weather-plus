import pytest
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

@pytest.mark.asyncio
async def test_mcp_flow():
    """
    End-to-end test validating the Client -> Server -> Tool flow.
    """
    # Define server parameters to run the server in a subprocess
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "weather_mcp"],
        env=dict(os.environ),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Initialize
            await session.initialize()

            # 2. List Tools
            result = await session.list_tools()
            tools = result.tools
            assert len(tools) >= 8  # We have 3 weather + 2 air quality + 3 time = 8 tools
            
            tool_names = [t.name for t in tools]
            assert "get_current_weather" in tool_names
            assert "get_air_quality" in tool_names
            assert "get_current_datetime" in tool_names

            # 3. Call a Tool (Time tool is safe/local)
            # Testing get_current_datetime
            time_result = await session.call_tool(
                "get_current_datetime",
                arguments={"timezone_name": "UTC"}
            )
            assert len(time_result.content) > 0
            assert time_result.content[0].type == "text"
            assert "T" in time_result.content[0].text  # Basic ISO format check or similar

            # 4. Call a Tool (Weather tool - hits Open-Meteo API)
            # This verifies external connectivity and the full chain
            weather_result = await session.call_tool(
                "get_current_weather",
                arguments={"city": "London"}
            )
            assert len(weather_result.content) > 0
            assert weather_result.content[0].type == "text"
            # The output should contain some weather info
            assert "London" in weather_result.content[0].text or "Temperature" in weather_result.content[0].text
