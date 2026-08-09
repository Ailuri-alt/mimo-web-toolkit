"""Dataclass для запроса генерации изображения."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ImageRequest:
    """Запрос на генерацию изображения.

    Attributes:
        purpose: Тип изображения (hero, background, illustration, product, portrait, custom).
        subject: Описание объекта изображения.
        filename: Имя итогового файла.
        style: Стиль изображения.
        aspect_ratio: Соотношение сторон.
        parameters: Дополнительные параметры генерации.
    """

    purpose: str
    subject: str
    filename: str
    style: str = "photorealistic"
    aspect_ratio: str = "16:9"
    parameters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Конвертирует запрос в словарь.

        Returns:
            Словарь с параметрами запроса.
        """
        return {
            "purpose": self.purpose,
            "subject": self.subject,
            "filename": self.filename,
            "style": self.style,
            "aspect_ratio": self.aspect_ratio,
            "parameters": self.parameters,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ImageRequest":
        """Создаёт запрос из словаря.

        Args:
            data: Словарь с параметрами запроса.

        Returns:
            Экземпляр ImageRequest.
        """
        return cls(
            purpose=data.get("purpose", "custom"),
            subject=data.get("subject", ""),
            filename=data.get("filename", "image.webp"),
            style=data.get("style", "photorealistic"),
            aspect_ratio=data.get("aspect_ratio", "16:9"),
            parameters=data.get("parameters", {}),
        )
