"""Dataclass для ответа генерации изображения."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ImageResponse:
    """Ответ на генерацию изображения.

    Attributes:
        success: Флаг успешности генерации.
        file: Путь к сгенерированному изображению.
        prompt_id: ID задачи в ComfyUI.
        error: Информация об ошибке.
        metadata: Дополнительные данные (описание, размеры и т.д.).
    """

    success: bool
    file: Path | None = None
    prompt_id: str | None = None
    error: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Конвертирует ответ в словарь.

        Returns:
            Словарь с результатом генерации.
        """
        result: dict[str, Any] = {"success": self.success}

        if self.file is not None:
            result["file"] = str(self.file)

        if self.prompt_id is not None:
            result["prompt_id"] = self.prompt_id

        if self.error is not None:
            result["error"] = self.error

        if self.metadata is not None:
            result.update(self.metadata)

        return result

    @classmethod
    def success(
        cls,
        file: Path,
        prompt_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "ImageResponse":
        """Создаёт успешный ответ.

        Args:
            file: Путь к изображению.
            prompt_id: ID задачи.
            metadata: Дополнительные данные.

        Returns:
            Экземпляр ImageResponse.
        """
        return cls(success=True, file=file, prompt_id=prompt_id, metadata=metadata)

    @classmethod
    def failure(cls, error_type: str, message: str) -> "ImageResponse":
        """Создаёт ответ с ошибкой.

        Args:
            error_type: Тип ошибки.
            message: Сообщение об ошибке.

        Returns:
            Экземпляр ImageResponse.
        """
        return cls(success=False, error={"type": error_type, "message": message})
