"""Базовый интерфейс ImageProvider.

Определяет контракт для всех провайдеров моделей генерации изображений.
Provider отвечает за взаимодействие с конкретной моделью, но НЕ выполняет HTTP-запросы.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from mcp_server.logger import get_logger

logger = get_logger(__name__)


class ImageProvider(ABC):
    """Абстрактный базовый класс для провайдеров моделей.

    Каждый провайдер инкапсулирует:
    - название модели;
    - формат файлов;
    - параметры запуска;
    - особенности VRAM;
    - специальные настройки.

    Provider НЕ выполняет HTTP-запросы.
    Для взаимодействия с ComfyUI используется ComfyClient.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Имя провайдера (например, 'flux-schnell', 'flux-dev-nf4')."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Название модели (например, 'flux1-schnell')."""
        ...

    @property
    @abstractmethod
    def vram_required(self) -> int:
        """Требуемый объём VRAM в ГБ."""
        ...

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        workflow_path: Path,
        parameters: dict[str, Any] | None = None,
    ) -> Path:
        """Генерирует изображение.

        Args:
            prompt: Промпт для генерации.
            workflow_path: Путь к JSON-workflow для ComfyUI.
            parameters: Дополнительные параметры генерации.

        Returns:
            Путь к сгенерированному изображению.
        """
        ...

    @abstractmethod
    def validate(self) -> bool:
        """Проверяет, что провайдер готов к работе.

        Returns:
            True, если провайдер готов, иначе False.
        """
        ...

    @abstractmethod
    def get_capabilities(self) -> dict[str, Any]:
        """Возвращает возможности провайдера.

        Returns:
            Словарь с информацией о возможностях модели.
        """
        ...
