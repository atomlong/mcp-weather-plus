class WeatherMcpError(Exception):
    """Base exception for weather-mcp errors."""
    pass

class ApiError(WeatherMcpError):
    """Raised when an external API call fails."""
    pass

class GeocodingError(WeatherMcpError):
    """Raised when geocoding fails (e.g., city not found)."""
    pass

class InvalidParameterError(WeatherMcpError):
    """Raised when input parameters are invalid."""
    pass
