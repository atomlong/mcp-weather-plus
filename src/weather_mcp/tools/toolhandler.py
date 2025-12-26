from abc import ABC, abstractmethod
from mcp.server import Server
from typing import Any, Dict

class ToolHandler(ABC):
    """Abstract base class for MCP tool handlers."""

    @abstractmethod
    def get_tools(self) -> list[Any]:
        """Returns a list of tools provided by this handler."""
        pass

    @abstractmethod
    async def handle_call(self, name: str, args: Dict[str, Any]) -> Any:
        """Handles a tool call."""
        pass
