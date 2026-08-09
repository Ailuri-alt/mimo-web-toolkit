"""Реестр MCP-инструментов проекта MiMo Web Toolkit.

Отвечает за регистрацию и управление инструментами.
Регистрация происходит автоматически при запуске сервера.
"""

from collections.abc import Awaitable, Callable
from typing import Any

from mcp import types

from mcp_server.exceptions import ToolRegistrationError
from mcp_server.logger import get_logger

logger = get_logger(__name__)


class ToolInfo:
    """Информация об MCP-инструменте.

    Attributes:
        name: Имя инструмента (например, generate_image).
        description: Описание назначения инструмента.
        input_schema: JSON Schema входных параметров.
        handler: Асинхронная функция-обработчик.
    """

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
        handler: Callable[..., Awaitable[types.CallToolResult]],
    ) -> None:
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.handler = handler

    def to_tool(self) -> types.Tool:
        """Конвертирует информацию в объект Tool для MCP.

        Returns:
            Экземпляр types.Tool.
        """
        return types.Tool(
            name=self.name,
            description=self.description,
            inputSchema=self.input_schema,
        )


class ToolRegistry:
    """Реестр MCP-инструментов.

    Управляет регистрацией и вызовом инструментов.
    Каждый инструмент — отдельный модуль с одной ответственностью.

    Attributes:
        tools: Словарь зарегистрированных инструментов.
    """

    def __init__(self) -> None:
        self.tools: dict[str, ToolInfo] = {}
        logger.info("ToolRegistry инициализирован")

    def register(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
        handler: Callable[..., Awaitable[types.CallToolResult]],
    ) -> None:
        """Регистрирует MCP-инструмент.

        Args:
            name: Имя инструмента (уникальное).
            description: Описание назначения.
            input_schema: JSON Schema входных параметров.
            handler: Асинхронная функция-обработчик.

        Raises:
            ToolRegistrationError: Если инструмент с таким именем уже зарегистрирован.
        """
        if name in self.tools:
            raise ToolRegistrationError(
                f"Инструмент уже зарегистрирован: {name}"
            )

        tool_info = ToolInfo(
            name=name,
            description=description,
            input_schema=input_schema,
            handler=handler,
        )
        self.tools[name] = tool_info
        logger.info("Зарегистрирован инструмент: %s", name)

    def get_tool(self, name: str) -> ToolInfo | None:
        """Возвращает информацию об инструменте по имени.

        Args:
            name: Имя инструмента.

        Returns:
            ToolInfo или None, если инструмент не найден.
        """
        return self.tools.get(name)

    def list_tools(self) -> list[types.Tool]:
        """Возвращает список всех зарегистрированных инструментов.

        Returns:
            Список объектов types.Tool.
        """
        return [tool.to_tool() for tool in self.tools.values()]

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> types.CallToolResult:
        """Вызывает MCP-инструмент.

        Args:
            name: Имя инструмента.
            arguments: Входные параметры.

        Returns:
            Результат выполнения инструмента.

        Raises:
            ToolRegistrationError: Если инструмент не найден.
        """
        tool = self.tools.get(name)
        if tool is None:
            raise ToolRegistrationError(f"Инструмент не найден: {name}")

        logger.info("Вызов инструмента: %s", name)
        result = await tool.handler(arguments)
        logger.info("Инструмент %s выполнен успешно", name)
        return result
