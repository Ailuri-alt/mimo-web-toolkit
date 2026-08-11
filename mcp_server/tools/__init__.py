"""MCP-инструменты MiMo Web Toolkit."""

from mcp_server.tools.generate_image import handler as generate_image
from mcp_server.tools.generate_image import INPUT_SCHEMA
from mcp_server.tools.generate_icons import handler as generate_icons
from mcp_server.tools.generate_icons import INPUT_SCHEMA as ICONS_INPUT_SCHEMA
from mcp_server.tools.generate_logo import handler as generate_logo
from mcp_server.tools.generate_logo import INPUT_SCHEMA as LOGO_INPUT_SCHEMA

__all__ = [
    "generate_image",
    "generate_icons",
    "generate_logo",
    "INPUT_SCHEMA",
    "ICONS_INPUT_SCHEMA",
    "LOGO_INPUT_SCHEMA",
]
