"""Тесты для PromptEngine."""

import pytest

from mcp_server.services.prompt_engine import PromptEngine
from mcp_server.exceptions import ConfigurationError


class TestPromptEngineBuildPrompt:
    """Тесты метода build_prompt()."""

    def test_build_prompt_hero(self) -> None:
        engine = PromptEngine()
        prompt = engine.build_prompt(
            purpose="hero",
            subject="luxury hotel",
            style="photorealistic",
        )
        assert "luxury hotel" in prompt
        assert "photorealistic" in prompt
        assert len(prompt) > 0

    def test_build_prompt_product(self) -> None:
        engine = PromptEngine()
        prompt = engine.build_prompt(
            purpose="product",
            subject="smart watch",
            style="studio photography",
        )
        assert "smart watch" in prompt

    def test_build_prompt_with_kwargs(self) -> None:
        engine = PromptEngine()
        prompt = engine.build_prompt(
            purpose="icons",
            subject="medical",
            style="outline",
            count="12",
            theme="healthcare",
        )
        assert "12" in prompt
        assert "healthcare" in prompt

    def test_build_prompt_invalid_purpose(self) -> None:
        engine = PromptEngine()
        with pytest.raises(ConfigurationError):
            engine.build_prompt(purpose="nonexistent", subject="test")

    def test_build_prompt_empty_subject(self) -> None:
        engine = PromptEngine()
        prompt = engine.build_prompt(purpose="hero", subject="")
        assert isinstance(prompt, str)


class TestPromptEngineNegativePrompt:
    """Тесты метода get_negative_prompt()."""

    def test_get_negative_prompt_hero(self) -> None:
        engine = PromptEngine()
        negative = engine.get_negative_prompt("hero")
        assert isinstance(negative, str)
        assert "blurry" in negative.lower()

    def test_get_negative_prompt_product(self) -> None:
        engine = PromptEngine()
        negative = engine.get_negative_prompt("product")
        assert isinstance(negative, str)

    def test_get_negative_prompt_invalid_purpose(self) -> None:
        engine = PromptEngine()
        with pytest.raises(ConfigurationError):
            engine.get_negative_prompt("nonexistent")
