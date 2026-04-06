"""Vérifie l'alignement ``pyproject.toml`` / ``default_metric_weights.py``."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

from baobab_mtg_deckbuilder.evaluation.default_metric_weights import default_metric_weights


class TestPyprojectDefaultWeightsMatch:
    """Documentation centralisée cohérente avec le code."""

    def test_toml_matches_module(self) -> None:
        """Les poids TOML sont identiques aux constantes Python."""
        root = Path(__file__).resolve().parents[3]
        pyproject = root / "pyproject.toml"
        with pyproject.open("rb") as handle:
            data = tomllib.load(handle)
        documented = data["tool"]["baobab_mtg_deckbuilder"]["evaluation"]["default_metric_weights"]
        # tomllib lit les nombres en float
        expected = default_metric_weights()
        assert len(documented) == len(expected)
        for key, value in expected.items():
            assert documented[key] == pytest.approx(value)
