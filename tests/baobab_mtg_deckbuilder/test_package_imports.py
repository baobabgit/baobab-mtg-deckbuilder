"""Tests for public package imports and metadata."""

import importlib
import importlib.metadata
from importlib.metadata import PackageNotFoundError

import baobab_mtg_deckbuilder as pkg
import pytest


class TestPackageImports:
    """Tests for the root package surface."""

    def test_import_package(self) -> None:
        """The package imports without side effects."""
        assert pkg.__doc__ is not None

    def test_version_is_non_empty_string(self) -> None:
        """``__version__`` is exposed as a non-empty string."""
        assert isinstance(pkg.__version__, str)
        assert len(pkg.__version__) > 0

    def test_version_fallback_when_distribution_missing(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """If distribution metadata is missing, ``__version__`` falls back to ``0.1.0``."""

        def _raise(_name: str) -> str:
            raise PackageNotFoundError(_name)

        monkeypatch.setattr(importlib.metadata, "version", _raise)
        importlib.reload(pkg)
        try:
            assert pkg.__version__ == "0.1.0"
        finally:
            monkeypatch.undo()
            importlib.reload(pkg)

    def test_public_exceptions_exported(self) -> None:
        """All project exceptions are available from the package root."""
        names = {
            "BaobabMtgDeckbuilderException",
            "DeckValidationException",
            "DeckGenerationException",
            "DeckOptimizationException",
            "DeckSimulationException",
            "DeckConfigurationException",
        }
        for name in names:
            assert hasattr(pkg, name)
            assert getattr(pkg, name).__module__.startswith("baobab_mtg_deckbuilder")

    def test_all_matches_exports(self) -> None:
        """``__all__`` lists symbols that exist on the package."""
        for name in pkg.__all__:
            assert hasattr(pkg, name)
