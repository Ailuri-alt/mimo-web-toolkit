"""Исключения проекта MiMo Web Toolkit.

Содержит специализированные исключения для всех компонентов системы.
"""


class MiMoToolkitError(Exception):
    """Базовое исключение для всех ошибок MiMo Toolkit."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ConfigurationError(MiMoToolkitError):
    """Ошибка загрузки или валидации конфигурации."""

    pass


class ComfyConnectionError(MiMoToolkitError):
    """Ошибка подключения к ComfyUI."""

    pass


class ComfyRequestError(MiMoToolkitError):
    """Ошибка выполнения запроса к ComfyUI."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.status_code = status_code
        super().__init__(message)


class WorkflowError(MiMoToolkitError):
    """Ошибка загрузки или выполнения workflow."""

    pass


class PromptError(MiMoToolkitError):
    """Ошибка формирования промпта."""

    pass


class ImageGenerationError(MiMoToolkitError):
    """Ошибка генерации изображения."""

    pass


class ImageProcessingError(MiMoToolkitError):
    """Ошибка обработки изображения."""

    pass


class ToolRegistrationError(MiMoToolkitError):
    """Ошибка регистрации MCP-инструмента."""

    pass
