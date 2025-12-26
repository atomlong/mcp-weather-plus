import httpx
from typing import Optional

_http_client: Optional[httpx.AsyncClient] = None

def get_http_client() -> httpx.AsyncClient:
    """
    Returns a shared instance of httpx.AsyncClient.
    Creates a new instance if one doesn't exist.
    """
    global _http_client
    if _http_client is None:
        _http_client = httpx.AsyncClient(timeout=30.0)
    return _http_client

async def close_http_client():
    """Closes the shared HTTP client if it exists."""
    global _http_client
    if _http_client:
        await _http_client.aclose()
        _http_client = None
