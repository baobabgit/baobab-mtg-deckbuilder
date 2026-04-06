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
        """If distribution metadata is missing, ``__version__`` falls back to ``0.8.0``."""

        def _raise(_name: str) -> str:
            raise PackageNotFoundError(_name)

        monkeypatch.setattr(importlib.metadata, "version", _raise)
        importlib.reload(pkg)
        try:
            assert pkg.__version__ == "0.8.0"
        finally:
            monkeypatch.undo()
            importlib.reload(pkg)

    def test_public_exceptions_exported(self) -> None:
        """All project exceptions are available from the package root."""
        names = {
            "BaobabMtgDeckbuilderException",
            "DeckValidationException",
            "DeckEvaluationException",
            "DeckGenerationException",
            "DeckOptimizationException",
            "DeckSimulationException",
            "DeckConfigurationException",
        }
        for name in names:
            assert hasattr(pkg, name)
            assert getattr(pkg, name).__module__.startswith("baobab_mtg_deckbuilder")

    def test_public_deck_model_exported(self) -> None:
        """Deck domain types are available from the package root."""
        names = {
            "Deck",
            "DeckCardEntry",
            "DeckSection",
            "DeckListView",
            "DeckSummary",
            "MAIN_DECK_SECTION_ID",
            "SIDEBOARD_SECTION_ID",
        }
        for name in names:
            assert hasattr(pkg, name)
            obj = getattr(pkg, name)
            if isinstance(obj, str):
                assert len(obj) > 0
            else:
                assert obj.__module__.startswith("baobab_mtg_deckbuilder")

    def test_public_validation_exported(self) -> None:
        """Validation types are available from the package root."""
        names = {
            "FormatDefinition",
            "ConstructedFormatDefinition",
            "LimitedFormatDefinition",
            "DeckConstraint",
            "DeckConstraintSet",
            "DeckValidationRule",
            "DeckValidationIssue",
            "DeckValidationIssueSeverity",
            "DeckValidationReport",
            "DEFAULT_BASIC_LAND_ORACLE_NAMES",
        }
        for name in names:
            assert hasattr(pkg, name)
            obj = getattr(pkg, name)
            if isinstance(obj, frozenset):
                assert len(obj) > 0
            else:
                assert isinstance(obj, type)
                assert obj.__module__.startswith("baobab_mtg_deckbuilder")

    def test_public_pool_exported(self) -> None:
        """Pool types and protocols are available from the package root."""
        names = {
            "CardPool",
            "CardPoolEntry",
            "CatalogCardProviderProtocol",
            "CollectionPoolProviderProtocol",
        }
        for name in names:
            assert hasattr(pkg, name)
            obj = getattr(pkg, name)
            assert obj.__module__.startswith("baobab_mtg_deckbuilder")

    def test_public_deck_statistics_exported(self) -> None:
        """Deck statistics types are available from the package root."""
        mana_cap = getattr(pkg, "MANA_CURVE_CAP")
        assert isinstance(mana_cap, int)
        assert mana_cap > 0
        names = {
            "CardAnalyticProfile",
            "CardAnalyticProviderProtocol",
            "DeckStatistics",
            "DeckStatisticsResult",
        }
        for name in names:
            assert hasattr(pkg, name)
            obj = getattr(pkg, name)
            assert obj.__module__.startswith("baobab_mtg_deckbuilder")

    def test_public_generation_exported(self) -> None:
        """Deck generation types and strategies are available from the package root."""
        names = {
            "DeckGenerationStrategy",
            "DeckGenerationRequest",
            "DeckGenerationResult",
            "DeckCandidate",
            "GreedyGenerationStrategy",
            "RandomSeededGenerationStrategy",
            "ConstrainedGenerationStrategy",
            "HybridGenerationStrategy",
            "build_maindeck_candidate",
            "main_minimum_for_format",
        }
        for name in names:
            assert hasattr(pkg, name)
            obj = getattr(pkg, name)
            assert obj.__module__.startswith("baobab_mtg_deckbuilder")

    def test_public_evaluation_exported(self) -> None:
        """Heuristic evaluation types are available from the package root."""
        names = {
            "DeckMetric",
            "DeckEvaluation",
            "DeckEvaluationBreakdown",
            "DeckEvaluationBreakdownLine",
            "DeckEvaluationExplanation",
            "DeckScore",
            "WeightedScoreAggregator",
            "default_metric_weights",
            "default_metric_weight_items",
            "ManaCurveEvaluator",
            "LandRatioEvaluator",
            "ColorBalanceEvaluator",
            "ManaBaseConsistencyEvaluator",
            "CardTypeBalanceEvaluator",
            "main_deck_card_quantity",
            "main_nonland_spell_quantity",
        }
        for name in names:
            assert hasattr(pkg, name)
            obj = getattr(pkg, name)
            if callable(obj):
                assert obj.__module__.startswith("baobab_mtg_deckbuilder")
            else:
                assert obj.__module__.startswith("baobab_mtg_deckbuilder")

    def test_all_matches_exports(self) -> None:
        """``__all__`` lists symbols that exist on the package."""
        for name in pkg.__all__:
            assert hasattr(pkg, name)
