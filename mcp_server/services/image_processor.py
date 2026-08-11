"""Image Processor — обработка и оптимизация изображений.

Отвечает за:
- проверку файла;
- оптимизацию формата;
- конвертацию в WebP/PNG/JPG;
- сохранение результата.

Image Processor НЕ выполняет HTTP-запросы.
"""

from pathlib import Path
from typing import Any

from PIL import Image

from mcp_server.exceptions import ImageProcessingError
from mcp_server.logger import get_logger

logger = get_logger(__name__)

DEFAULT_OUTPUT_DIR = Path("assets/optimized")
SUPPORTED_FORMATS = {"webp", "png", "jpg", "jpeg"}
DEFAULT_QUALITY = 85
DEFAULT_FORMAT = "webp"


class ImageProcessor:
    """Обработчик изображений.

    Инкапсулирует логику обработки и оптимизации изображений.

    Attributes:
        output_dir: Каталог для сохранения обработанных изображений.
        default_format: Формат по умолчанию.
        default_quality: Качество по умолчанию (1-100).
    """

    def __init__(
        self,
        output_dir: Path | None = None,
        default_format: str = DEFAULT_FORMAT,
        default_quality: int = DEFAULT_QUALITY,
    ) -> None:
        """Инициализирует Image Processor.

        Args:
            output_dir: Каталог для сохранения. Если None — assets/optimized/.
            default_format: Формат по умолчанию (webp, png, jpg).
            default_quality: Качество по умолчанию (1-100).
        """
        self.output_dir = output_dir or DEFAULT_OUTPUT_DIR
        self.default_format = default_format
        self.default_quality = default_quality
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(
            "ImageProcessor инициализирован: output=%s, format=%s, quality=%d",
            self.output_dir,
            default_format,
            default_quality,
        )

    def process(
        self,
        input_path: Path,
        output_filename: str | None = None,
        output_format: str | None = None,
        quality: int | None = None,
    ) -> Path:
        """Обрабатывает изображение.

        Args:
            input_path: Путь к входному изображению.
            output_filename: Имя выходного файла. Если None — на основе входного.
            output_format: Формат выходного файла. Если None — default_format.
            quality: Качество (1-100). Если None — default_quality.

        Returns:
            Путь к обработанному изображению.

        Raises:
            ImageProcessingError: Если не удалось обработать изображение.
        """
        if not input_path.exists():
            raise ImageProcessingError(f"Файл не найден: {input_path}")

        fmt = output_format or self.default_format
        qual = quality or self.default_quality

        if fmt not in SUPPORTED_FORMATS:
            raise ImageProcessingError(
                f"Неподдерживаемый формат: {fmt}. Допустимые: {SUPPORTED_FORMATS}"
            )

        try:
            with Image.open(input_path) as img:
                if fmt in ("jpg", "jpeg") and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                if output_filename is None:
                    output_filename = f"{input_path.stem}.{fmt}"

                output_path = self.output_dir / output_filename

                save_kwargs: dict[str, Any] = {}
                if fmt == "webp":
                    save_kwargs["quality"] = qual
                    save_kwargs["method"] = 6
                elif fmt in ("jpg", "jpeg"):
                    save_kwargs["quality"] = qual
                    save_kwargs["optimize"] = True
                elif fmt == "png":
                    save_kwargs["optimize"] = True

                pil_format = "JPEG" if fmt in ("jpg", "jpeg") else fmt.upper()
                img.save(output_path, format=pil_format, **save_kwargs)

        except Exception as e:
            raise ImageProcessingError(f"Ошибка обработки изображения: {e}") from e

        original_size = input_path.stat().st_size
        optimized_size = output_path.stat().st_size
        reduction = (1 - optimized_size / original_size) * 100 if original_size > 0 else 0

        logger.info(
            "Изображение обработано: %s -> %s (%.1f%% снижение)",
            input_path.name,
            output_path.name,
            reduction,
        )

        return output_path

    def get_info(self, image_path: Path) -> dict[str, Any]:
        """Возвращает информацию об изображении.

        Args:
            image_path: Путь к изображению.

        Returns:
            Словарь с информацией (format, size, mode, width, height).

        Raises:
            ImageProcessingError: Если не удалось прочитать изображение.
        """
        if not image_path.exists():
            raise ImageProcessingError(f"Файл не найден: {image_path}")

        try:
            with Image.open(image_path) as img:
                return {
                    "format": img.format,
                    "mode": img.mode,
                    "width": img.width,
                    "height": img.height,
                    "size_bytes": image_path.stat().st_size,
                }
        except Exception as e:
            raise ImageProcessingError(f"Ошибка чтения изображения: {e}") from e
