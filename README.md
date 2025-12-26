# Weather MCP Server

A Model Context Protocol (MCP) server that provides real-time weather forecasts, air quality data, and timezone information. Built with Python and integrated with the [Open-Meteo API](https://open-meteo.com/).

## 🌟 Features

-   **Weather Forecasts**: Get current weather, hourly forecasts, and detailed meteorological data.
-   **Air Quality**: Access real-time air quality index (AQI), PM2.5, PM10, and pollutant concentrations.
-   **Time Utilities**: Current time lookups and timezone conversions.
-   **Dual Transport**: Supports both standard input/output (`stdio`) and Streamable HTTP transports.
-   **No API Key Required**: Powered by Open-Meteo's open data APIs.

## 🛠️ Available Tools

### Weather Tools
-   `get_current_weather`: Get current weather metrics (temperature, humidity, wind, etc.) for a city.
-   `get_weather_by_datetime_range`: Get hourly weather trends for a specific date range.
-   `get_weather_details`: Get comprehensive raw weather data in JSON format.

### Air Quality Tools
-   `get_air_quality`: Get current air quality metrics and AQI assessment.
-   `get_air_quality_details`: Get detailed pollutant data (PM2.5, PM10, Ozone, etc.) in JSON format.

### Time Tools
-   `get_current_datetime`: Get the current date and time for a specific timezone (e.g., "Asia/Shanghai").
-   `get_timezone_info`: Get detailed information about a timezone (offset, DST status).
-   `convert_time`: Convert a date/time string from one timezone to another.

## 🚀 Installation & Usage

### Prerequisites
-   Python 3.12+
-   [uv](https://github.com/astral-sh/uv) (recommended for dependency management)

### Local Development

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd weather-mcp
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

3.  **Run the server (stdio mode - default):**
    ```bash
    uv run mcp-weather-plus
    ```

4.  **Run the server (HTTP mode):**
    ```bash
    uv run mcp-weather-plus --mode streamable-http --port 8080
    ```

### Docker

1.  **Build the image:**
    ```bash
    docker build -t mcp-weather-plus .
    ```

2.  **Run container (stdio):**
    ```bash
    docker run -i mcp-weather-plus
    ```

3.  **Run container (HTTP):**
    ```bash
    docker run -p 8080:8080 mcp-weather-plus --mode streamable-http --port 8080
    ```

## 🧪 Testing

Run the test suite using `pytest`:

```bash
uv run pytest
```

## 📂 Project Structure

```text
weather-mcp/
├── src/mcp_weather_plus/       # Source code
│   ├── services/          # Business logic and API integrations
│   ├── tools/             # MCP Tool handlers
│   ├── server.py          # Server setup and transport logic
│   └── ...
├── tests/                 # Unit tests
├── pyproject.toml         # Project configuration and dependencies
└── Dockerfile             # Docker build definition
```

## 🤖 Configuration for AI Agents

You can easily use this MCP server with various AI agents like Claude Desktop, VS Code (Cline), and Cursor.

The recommended way to run this server is using `uvx`, which downloads and runs the latest version without manual installation.

### Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uvx",
      "args": [
        "mcp-weather-plus"
      ]
    }
  }
}
```

### VS Code (Cline)

Add the following to your `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uvx",
      "args": [
        "mcp-weather-plus"
      ]
    }
  }
}
```

### Cursor

1.  Go to **Settings** -> **Features** -> **MCP**.
2.  Click **Add New MCP Server**.
3.  Enter the following:
    *   **Name**: `weather`
    *   **Type**: `stdio`
    *   **Command**: `uvx`
    *   **Args**: `mcp-weather-plus`

### Connecting via Streamable HTTP (Remote/Docker)

If you are running the server via Docker or on a remote machine using the `streamable-http` mode (e.g., `uv run mcp-weather-plus --mode streamable-http --port 8080`), you can connect to it using the SSE configuration.

**Claude Desktop Config:**

```json
{
  "mcpServers": {
    "weather-remote": {
      "url": "http://localhost:8080/sse"
    }
  }
}
```

---

## 📄 License

This project is licensed under the MIT License. Data provided by [Open-Meteo](https://open-meteo.com/) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
