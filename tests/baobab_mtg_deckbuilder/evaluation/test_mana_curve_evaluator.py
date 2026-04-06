"""Tests for :class:`ManaCurveEvaluator`."""

from baobab_mtg_deckbuilder.evaluation.mana_curve_evaluator import ManaCurveEvaluator
from tests.baobab_mtg_deckbuilder.evaluation.deck_statistics_result_factory import (
    deck_statistics_result,
)


class TestManaCurveEvaluator:
    """Favorable, défavorable et neutre."""

    def test_neutral_without_spells(self) -> None:
        """Sans sorts, score neutre et explication explicite."""
        stats = deck_statistics_result(
            main_land_quantity=24,
            main_quantity_by_english_name={"Island": 24},
        )
        metric = ManaCurveEvaluator().evaluate(stats)
        assert metric.metric_id == "mana_curve_similarity"
        assert metric.normalized_score == 0.5
        assert "Aucun sort" in metric.explanation.summary
        assert len(metric.explanation.details) >= 1

    def test_favorable_matches_ideal_template(self) -> None:
        """Distribution identique au gabarit interne → score maximal."""
        curve = {0: 6, 1: 14, 2: 26, 3: 24, 4: 14, 5: 8, 6: 5, 7: 3}
        stats = deck_statistics_result(
            main_spell_mana_curve=curve,
            main_quantity_by_english_name={"x": 100},
        )
        metric = ManaCurveEvaluator().evaluate(stats)
        assert metric.normalized_score == 1.0
        assert metric.raw_score == 100.0
        assert "1.00" in metric.explanation.summary
        assert "Pic de courbe" in metric.explanation.details[1]

    def test_unfavorable_single_high_bucket(self) -> None:
        """Tout le coût dans le bac haut → score faible."""
        stats = deck_statistics_result(
            main_spell_mana_curve={7: 40},
            main_quantity_by_english_name={"Spell": 40},
        )
        metric = ManaCurveEvaluator().evaluate(stats)
        assert metric.normalized_score < 0.2
        assert metric.explanation.details[0].startswith("Sorts non-terrain")

    def test_explanation_includes_unknown_and_missing(self) -> None:
        """Les détails mentionnent CMC inconnu et profils manquants."""
        stats = deck_statistics_result(
            main_spell_mana_curve={1: 10},
            main_spell_mana_value_unknown_quantity=2,
            main_profile_missing_quantity=5,
            main_quantity_by_english_name={"A": 17},
        )
        metric = ManaCurveEvaluator().evaluate(stats)
        joined = " ".join(metric.explanation.details)
        assert "CMC inconnu" in joined
        assert "Profils manquants" in joined
