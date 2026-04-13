"""Tests for CLI plugin integration."""

import re

import pytest
import typer
from typer.testing import CliRunner

from plugins.icrc2023 import ICRC2023Schema
from titanite.cli import _load_schema_class, app

runner = CliRunner()


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def test_load_schema_class_with_valid_plugin():
    """_load_schema_class successfully loads ICRC2023Schema."""
    schema_class = _load_schema_class("plugins.icrc2023.ICRC2023Schema")
    assert schema_class is ICRC2023Schema
    schema = schema_class()
    assert isinstance(schema, ICRC2023Schema)


def test_load_schema_class_with_invalid_module():
    """_load_schema_class raises Exit on invalid module."""
    with pytest.raises(typer.Exit):
        _load_schema_class("plugins.nonexistent.Schema")


def test_load_schema_class_with_invalid_class():
    """_load_schema_class raises Exit on invalid class name."""
    with pytest.raises(typer.Exit):
        _load_schema_class("plugins.icrc2023.NonexistentSchema")


def test_load_schema_class_with_invalid_format():
    """_load_schema_class raises Exit on invalid plugin name format."""
    with pytest.raises(typer.Exit):
        _load_schema_class("invalid_format")


def test_cli_prepare_accepts_plugin_option():
    """prepare command accepts --plugin option (integration test)."""
    # This test verifies the command signature allows --plugin option
    # without actually running the full pipeline
    result = runner.invoke(app, ["prepare", "--help"])
    assert result.exit_code == 0
    assert "--plugin" in _strip_ansi(result.stdout)
