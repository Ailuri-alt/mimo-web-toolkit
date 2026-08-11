"""MCP-инструменты MiMo Web Toolkit."""

from mcp_server.tools.generate_image import handler as generate_image
from mcp_server.tools.generate_image import INPUT_SCHEMA
from mcp_server.tools.generate_logo import handler as generate_logo
from mcp_server.tools.generate_logo import INPUT_SCHEMA as LOGO_INPUT_SCHEMA

__all__ = ["generate_image", "generate_logo", "INPUT_SCHEMA", "LOGO_INPUT_SCHEMA"]
