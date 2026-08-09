"""MCP-инструменты MiMo Web Toolkit."""

from mcp_server.tools.generate_image import handler as generate_image
from mcp_server.tools.generate_image import INPUT_SCHEMA

__all__ = ["generate_image", "INPUT_SCHEMA"]
