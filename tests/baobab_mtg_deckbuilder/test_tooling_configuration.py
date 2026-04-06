"""Tests ensuring quality tooling is configured in ``pyproject.toml``."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

import pytest


class TestToolingConfiguration:
    """Guards for centralized tool configuration."""

    @pytest.fixture(name="pyproject_data")
    def fixture_pyproject_data(self) -> dict[str, Any]:
        """Load parsed ``pyproject.toml`` from the repository root."""
        root = Path(__file__).resolve().parents[2]
        raw = (root / "pyproject.toml").read_text(encoding="utf-8")
        data: dict[str, Any] = tomllib.loads(raw)
        return data

    def test_pytest_addopts_include_coverage(self, pyproject_data: dict[str, Any]) -> None:
        """Pytest is wired to coverage reports under ``docs/tests/coverage``."""
        opts = pyproject_data["tool"]["pytest"]["ini_options"]["addopts"]
        assert any("--cov=baobab_mtg_deckbuilder" == o for o in opts)
        assert any(o.startswith("--cov-report=html:") for o in opts)
        assert any("docs/tests/coverage/html" in o for o in opts)
        assert any(o.startswith("--cov-report=xml:") for o in opts)
        assert any("docs/tests/coverage/coverage.xml" in o for o in opts)

    def test_coverage_fail_under_at_least_90(self, pyproject_data: dict[str, Any]) -> None:
        """Coverage enforces at least 90% line coverage."""
        fail_under = pyproject_data["tool"]["coverage"]["report"]["fail_under"]
        assert fail_under >= 90

    def test_coverage_data_file_under_docs_tests_coverage(
        self, pyproject_data: dict[str, Any]
    ) -> None:
        """Coverage data file lives under ``docs/tests/coverage``."""
        data_file = pyproject_data["tool"]["coverage"]["run"]["data_file"]
        assert "docs/tests/coverage" in data_file

    def test_mypy_strict_enabled(self, pyproject_data: dict[str, Any]) -> None:
        """Mypy runs in strict mode for the main package."""
        assert pyproject_data["tool"]["mypy"]["strict"] is True

    def test_black_line_length_100(self, pyproject_data: dict[str, Any]) -> None:
        """Black matches the 100-character project limit."""
        assert pyproject_data["tool"]["black"]["line-length"] == 100

    def test_flake8_line_length_100(self, pyproject_data: dict[str, Any]) -> None:
        """Flake8 matches the 100-character project limit."""
        assert pyproject_data["tool"]["flake8"]["max-line-length"] == 100
