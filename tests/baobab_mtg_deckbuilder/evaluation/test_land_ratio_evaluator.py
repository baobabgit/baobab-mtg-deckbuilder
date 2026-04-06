"""Tests for :class:`LandRatioEvaluator`."""

from baobab_mtg_deckbuilder.evaluation.land_ratio_evaluator import LandRatioEvaluator
from tests.baobab_mtg_deckbuilder.evaluation.deck_statistics_result_factory import (
    deck_statistics_result,
)


class TestLandRatioEvaluator:
    """Ratio terrains / main."""

    def test_neutral_empty_main(self) -> None:
        """Main vide → neutre."""
        stats = deck_statistics_result()
        metric = LandRatioEvaluator().evaluate(stats)
        assert metric.normalized_score == 0.5
        assert "vide" in metric.explanation.summary.lower()

    def test_favorable_near_target(self) -> None:
        """38 % de terrains sur 50 cartes → score maximal."""
        stats = deck_statistics_result(
            main_land_quantity=19,
            main_quantity_by_english_name={"L": 19, "S": 31},
        )
        metric = LandRatioEvaluator().evaluate(stats)
        assert metric.normalized_score == 1.0
        assert "19 sur 50" in metric.explanation.details[0]

    def test_unfavorable_too_few_lands(self) -> None:
        """10 % de terrains → score faible."""
        stats = deck_statistics_result(
            main_land_quantity=6,
            main_quantity_by_english_name={"L": 6, "S": 54},
        )
        metric = LandRatioEvaluator().evaluate(stats)
        assert metric.normalized_score < 0.5

    def test_explanation_warns_on_missing_profiles(self) -> None:
        """Une ligne alerte si des profils manquent."""
        stats = deck_statistics_result(
            main_land_quantity=20,
            main_profile_missing_quantity=10,
            main_quantity_by_english_name={"L": 20, "X": 40},
        )
        metric = LandRatioEvaluator().evaluate(stats)
        assert any("Profils manquants" in d for d in metric.explanation.details)
