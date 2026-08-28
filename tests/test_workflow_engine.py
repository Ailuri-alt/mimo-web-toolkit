"""Тесты для WorkflowEngine."""

import pytest
from pathlib import Path

from mcp_server.services.workflow_engine import WorkflowEngine
from mcp_server.exceptions import ConfigurationError


class TestWorkflowEngineGetWorkflowPath:
    """Тесты метода get_workflow_path()."""

    def test_get_workflow_path_hero(self) -> None:
        engine = WorkflowEngine()
        path = engine.get_workflow_path("hero")
        assert path.exists()
        assert path.suffix == ".json"

    def test_get_workflow_path_product(self) -> None:
        engine = WorkflowEngine()
        path = engine.get_workflow_path("product")
        assert path.exists()

    def test_get_workflow_path_invalid_purpose(self) -> None:
        engine = WorkflowEngine()
        with pytest.raises(ConfigurationError):
            engine.get_workflow_path("nonexistent")


class TestWorkflowEngineLoadWorkflow:
    """Тесты метода load_workflow()."""

    def test_load_workflow_hero(self) -> None:
        engine = WorkflowEngine()
        workflow = engine.load_workflow("hero")
        assert isinstance(workflow, dict)
        assert len(workflow) > 0

    def test_load_workflow_has_nodes(self) -> None:
        engine = WorkflowEngine()
        workflow = engine.load_workflow("hero")
        for node_id, node in workflow.items():
            assert isinstance(node, dict)
            assert "class_type" in node
            assert "inputs" in node


class TestWorkflowEngineGenerationParams:
    """Тесты метода get_generation_params()."""

    def test_get_generation_params_hero(self) -> None:
        engine = WorkflowEngine()
        params = engine.get_generation_params("hero")
        assert "sampler" in params
        assert "scheduler" in params
        assert "cfg" in params
        assert "steps" in params

    def test_get_generation_params_background(self) -> None:
        engine = WorkflowEngine()
        params = engine.get_generation_params("background")
        assert params["steps"] == 15


class TestWorkflowEngineDefaults:
    """Тесты методов default_style и default_aspect_ratio."""

    def test_get_default_style(self) -> None:
        engine = WorkflowEngine()
        style = engine.get_default_style("hero")
        assert style == "photorealistic"

    def test_get_default_aspect_ratio(self) -> None:
        engine = WorkflowEngine()
        ratio = engine.get_default_aspect_ratio("hero")
        assert ratio == "16:9"

    def test_list_available_purposes(self) -> None:
        engine = WorkflowEngine()
        purposes = engine.list_available_purposes()
        assert "hero" in purposes
        assert "product" in purposes
        assert "portrait" in purposes
