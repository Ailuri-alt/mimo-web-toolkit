"""Тесты для ImageProcessor."""

import pytest
from pathlib import Path

from mcp_server.services.image_processor import ImageProcessor
from mcp_server.exceptions import ImageProcessingError


class TestImageProcessorProcess:
    """Тесты метода process()."""

    def test_process_png_to_webp(self, test_image: Path, tmp_path: Path) -> None:
        processor = ImageProcessor(output_dir=tmp_path)
        result = processor.process(test_image, output_format="webp")
        assert result.exists()
        assert result.suffix == ".webp"

    def test_process_webp_to_png(self, test_image_webp: Path, tmp_path: Path) -> None:
        processor = ImageProcessor(output_dir=tmp_path)
        result = processor.process(test_image_webp, output_format="png")
        assert result.exists()
        assert result.suffix == ".png"

    def test_process_with_custom_filename(self, test_image: Path, tmp_path: Path) -> None:
        processor = ImageProcessor(output_dir=tmp_path)
        result = processor.process(test_image, output_filename="custom.webp")
        assert result.name == "custom.webp"

    def test_process_nonexistent_file(self, tmp_path: Path) -> None:
        processor = ImageProcessor(output_dir=tmp_path)
        with pytest.raises(ImageProcessingError, match="Файл не найден"):
            processor.process(Path("nonexistent.png"))

    def test_process_invalid_format(self, test_image: Path, tmp_path: Path) -> None:
        processor = ImageProcessor(output_dir=tmp_path)
        with pytest.raises(ImageProcessingError, match="Неподдерживаемый формат"):
            processor.process(test_image, output_format="bmp")


class TestImageProcessorResize:
    """Тесты метода resize()."""

    def test_resize_2x(self, test_image: Path, tmp_path: Path) -> None:
        processor = ImageProcessor(output_dir=tmp_path)
        result = processor.resize(test_image, scale=2)
        assert result.exists()

    def test_resize_1x(self, test_image: Path, tmp_path: Path) -> None:
        processor = ImageProcessor(output_dir=tmp_path)
        result = processor.resize(test_image, scale=1)
        assert result.exists()

    def test_resize_nonexistent_file(self, tmp_path: Path) -> None:
        processor = ImageProcessor(output_dir=tmp_path)
        with pytest.raises(ImageProcessingError, match="Файл не найден"):
            processor.resize(Path("nonexistent.png"), scale=2)

    def test_resize_invalid_scale(self, test_image: Path, tmp_path: Path) -> None:
        processor = ImageProcessor(output_dir=tmp_path)
        with pytest.raises(ImageProcessingError, match="Множитель"):
            processor.resize(test_image, scale=0)

    def test_resize_scale_too_large(self, test_image: Path, tmp_path: Path) -> None:
        processor = ImageProcessor(output_dir=tmp_path)
        with pytest.raises(ImageProcessingError, match="Множитель"):
            processor.resize(test_image, scale=5)


class TestImageProcessorGetInfo:
    """Тесты метода get_info()."""

    def test_get_info(self, test_image: Path) -> None:
        processor = ImageProcessor()
        info = processor.get_info(test_image)
        assert info["format"] == "PNG"
        assert info["width"] == 100
        assert info["height"] == 100

    def test_get_info_nonexistent_file(self) -> None:
        processor = ImageProcessor()
        with pytest.raises(ImageProcessingError, match="Файл не найден"):
            processor.get_info(Path("nonexistent.png"))
