"""Tests for :class:`ColorBalanceEvaluator`."""

from baobab_mtg_deckbuilder.evaluation.color_balance_evaluator import ColorBalanceEvaluator
from tests.baobab_mtg_deckbuilder.evaluation.deck_statistics_result_factory import (
    deck_statistics_result,
)


class TestColorBalanceEvaluator:
    """Équilibre WUBRG."""

    def test_neutral_no_wubrg(self) -> None:
        """Sans pips WUBRG → neutre."""
        stats = deck_statistics_result(
            main_color_quantity_by_label={"C": 40, "?": 2},
        )
        metric = ColorBalanceEvaluator().evaluate(stats)
        assert metric.normalized_score == 0.5
        assert "Aucun pip WUBRG" in metric.explanation.summary

    def test_favorable_mono_color(self) -> None:
        """Mono : score 1,0."""
        stats = deck_statistics_result(
            main_color_quantity_by_label={"R": 40},
        )
        metric = ColorBalanceEvaluator().evaluate(stats)
        assert metric.normalized_score == 1.0
        assert "Mono-couleur" in metric.explanation.summary

    def test_favorable_dual_balanced(self) -> None:
        """Deux couleurs 50/50 → entropie maximale pour n=2."""
        stats = deck_statistics_result(
            main_color_quantity_by_label={"U": 20, "B": 20},
        )
        metric = ColorBalanceEvaluator().evaluate(stats)
        assert metric.normalized_score == 1.0

    def test_less_favorable_skewed_dual(self) -> None:
        """Deux couleurs déséquilibrées → entropie plus basse."""
        balanced = ColorBalanceEvaluator().evaluate(
            deck_statistics_result(main_color_quantity_by_label={"G": 15, "W": 15})
        )
        skewed = ColorBalanceEvaluator().evaluate(
            deck_statistics_result(main_color_quantity_by_label={"G": 28, "W": 2})
        )
        assert skewed.normalized_score < balanced.normalized_score

    def test_explanation_lists_unknown_and_colorless(self) -> None:
        """Les détails citent C et ?."""
        stats = deck_statistics_result(
            main_color_quantity_by_label={"R": 10, "C": 3, "?": 1},
        )
        metric = ColorBalanceEvaluator().evaluate(stats)
        details = " ".join(metric.explanation.details)
        assert "« ? »" in details or "?" in details
        assert "« C »" in details or "C" in details
