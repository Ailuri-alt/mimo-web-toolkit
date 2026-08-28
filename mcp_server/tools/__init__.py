"""MCP-инструменты MiMo Web Toolkit."""

from mcp_server.tools.convert_svg import handler as convert_svg
from mcp_server.tools.convert_svg import INPUT_SCHEMA as CONVERT_SVG_INPUT_SCHEMA
from mcp_server.tools.describe_image import handler as describe_image
from mcp_server.tools.describe_image import INPUT_SCHEMA as DESCRIBE_IMAGE_INPUT_SCHEMA
from mcp_server.tools.generate_background import handler as generate_background
from mcp_server.tools.generate_background import INPUT_SCHEMA as BACKGROUND_INPUT_SCHEMA
from mcp_server.tools.generate_icons import handler as generate_icons
from mcp_server.tools.generate_icons import INPUT_SCHEMA as ICONS_INPUT_SCHEMA
from mcp_server.tools.generate_image import handler as generate_image
from mcp_server.tools.generate_image import INPUT_SCHEMA
from mcp_server.tools.generate_logo import handler as generate_logo
from mcp_server.tools.generate_logo import INPUT_SCHEMA as LOGO_INPUT_SCHEMA
from mcp_server.tools.generate_product_image import handler as generate_product_image
from mcp_server.tools.generate_product_image import INPUT_SCHEMA as PRODUCT_IMAGE_INPUT_SCHEMA
from mcp_server.tools.generate_team_photo import handler as generate_team_photo
from mcp_server.tools.generate_team_photo import INPUT_SCHEMA as TEAM_PHOTO_INPUT_SCHEMA
from mcp_server.tools.optimize_image import handler as optimize_image
from mcp_server.tools.optimize_image import INPUT_SCHEMA as OPTIMIZE_IMAGE_INPUT_SCHEMA
from mcp_server.tools.remove_background import handler as remove_background
from mcp_server.tools.remove_background import INPUT_SCHEMA as REMOVE_BACKGROUND_INPUT_SCHEMA
from mcp_server.tools.upscale_image import handler as upscale_image
from mcp_server.tools.upscale_image import INPUT_SCHEMA as UPSCALE_IMAGE_INPUT_SCHEMA

__all__ = [
    "convert_svg",
    "describe_image",
    "generate_background",
    "generate_icons",
    "generate_image",
    "generate_logo",
    "generate_product_image",
    "generate_team_photo",
    "optimize_image",
    "remove_background",
    "upscale_image",
    "CONVERT_SVG_INPUT_SCHEMA",
    "DESCRIBE_IMAGE_INPUT_SCHEMA",
    "BACKGROUND_INPUT_SCHEMA",
    "ICONS_INPUT_SCHEMA",
    "INPUT_SCHEMA",
    "LOGO_INPUT_SCHEMA",
    "OPTIMIZE_IMAGE_INPUT_SCHEMA",
    "PRODUCT_IMAGE_INPUT_SCHEMA",
    "TEAM_PHOTO_INPUT_SCHEMA",
    "REMOVE_BACKGROUND_INPUT_SCHEMA",
    "UPSCALE_IMAGE_INPUT_SCHEMA",
]
