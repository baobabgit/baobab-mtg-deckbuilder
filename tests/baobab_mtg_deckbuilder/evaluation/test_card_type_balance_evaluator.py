"""Tests for :class:`CardTypeBalanceEvaluator`."""

import pytest

from baobab_mtg_deckbuilder.evaluation.card_type_balance_evaluator import (
    CardTypeBalanceEvaluator,
)
from tests.baobab_mtg_deckbuilder.evaluation.deck_statistics_result_factory import (
    deck_statistics_result,
)


class TestCardTypeBalanceEvaluator:
    """Diversité des types."""

    def test_neutral_no_typed_categories(self) -> None:
        """Aucun type hors « ? » → neutre."""
        stats = deck_statistics_result(
            main_type_quantity_by_label={"?": 40},
        )
        metric = CardTypeBalanceEvaluator().evaluate(stats)
        assert metric.normalized_score == 0.5
        assert "Aucun type catégorisé" in metric.explanation.summary

    def test_mono_type_moderate_score(self) -> None:
        """Un seul type → score modéré 0,65."""
        stats = deck_statistics_result(
            main_type_quantity_by_label={"Creature": 40},
        )
        metric = CardTypeBalanceEvaluator().evaluate(stats)
        assert metric.normalized_score == CardTypeBalanceEvaluator._MONO_TYPE_SCORE
        assert "Une seule catégorie" in metric.explanation.summary

    def test_favorable_balanced_multi_types(self) -> None:
        """Plusieurs types équilibrés → entropie élevée."""
        stats = deck_statistics_result(
            main_type_quantity_by_label={
                "Creature": 20,
                "Instant": 20,
                "Sorcery": 20,
            },
        )
        metric = CardTypeBalanceEvaluator().evaluate(stats)
        assert metric.normalized_score == pytest.approx(1.0)

    def test_neutral_zero_quantities_with_labels(self) -> None:
        """Libellés présents mais quantités nulles → neutre."""
        stats = deck_statistics_result(
            main_type_quantity_by_label={"Creature": 0},
        )
        metric = CardTypeBalanceEvaluator().evaluate(stats)
        assert metric.normalized_score == 0.5

    def test_less_favorable_concentrated(self) -> None:
        """Même nombre de types mais concentration extrême."""
        balanced = CardTypeBalanceEvaluator().evaluate(
            deck_statistics_result(
                main_type_quantity_by_label={"Instant": 10, "Sorcery": 10},
            )
        )
        concentrated = CardTypeBalanceEvaluator().evaluate(
            deck_statistics_result(
                main_type_quantity_by_label={"Instant": 19, "Sorcery": 1},
            )
        )
        assert concentrated.normalized_score < balanced.normalized_score

    def test_explanation_includes_unknown_types(self) -> None:
        """Les détails mentionnent les exemplaires « ? »."""
        stats = deck_statistics_result(
            main_type_quantity_by_label={"Artifact": 10, "?": 2},
        )
        metric = CardTypeBalanceEvaluator().evaluate(stats)
        assert any("« ? »" in d or "?" in d for d in metric.explanation.details)
