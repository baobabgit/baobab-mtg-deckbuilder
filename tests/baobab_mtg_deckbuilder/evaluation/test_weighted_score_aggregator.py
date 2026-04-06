"""Tests for :class:`WeightedScoreAggregator`."""

import pytest

from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)
from baobab_mtg_deckbuilder.evaluation.deck_metric import DeckMetric
from baobab_mtg_deckbuilder.evaluation.default_metric_weights import default_metric_weights
from baobab_mtg_deckbuilder.evaluation.weighted_score_aggregator import (
    WeightedScoreAggregator,
)
from baobab_mtg_deckbuilder.exceptions.deck_evaluation_exception import (
    DeckEvaluationException,
)


def _m(
    mid: str,
    name: str,
    norm: float,
    raw: float = 50.0,
) -> DeckMetric:
    return DeckMetric(
        metric_id=mid,
        display_name=name,
        raw_score=raw,
        normalized_score=norm,
        explanation=DeckEvaluationExplanation(title=name, summary=name, details=()),
    )


class TestWeightedScoreAggregator:
    """Agrégation, bonus / pénalité, breakdown stable, explications."""

    def test_weighted_average_controlled(self) -> None:
        """Deux métriques 0,5 / 0,5 avec scores 1 et 0 → moyenne 0,5."""
        agg = WeightedScoreAggregator(
            weights={"a": 0.5, "b": 0.5},
        )
        ev = agg.aggregate(
            (
                _m("a", "A", 1.0, 100.0),
                _m("b", "B", 0.0, 0.0),
            )
        )
        assert ev.score.weighted_average == pytest.approx(0.5)
        assert ev.score.final_score == pytest.approx(0.5)
        assert ev.breakdown.weighted_sum == pytest.approx(0.5)

    def test_bonus_and_penalty(self) -> None:
        """Bonus et pénalité modifient le score final avec clamp."""
        agg = WeightedScoreAggregator(weights={"x": 1.0}, global_bonus=0.1, global_penalty=0.05)
        ev = agg.aggregate((_m("x", "X", 0.5),))
        assert ev.score.weighted_average == pytest.approx(0.5)
        assert ev.score.global_bonus == pytest.approx(0.1)
        assert ev.score.global_penalty == pytest.approx(0.05)
        assert ev.score.final_score == pytest.approx(0.55)

    def test_clamp_high_and_explanation_note(self) -> None:
        """Agrégat brut > 1 → clamp et mention dans les détails."""
        agg = WeightedScoreAggregator(weights={"x": 1.0}, global_bonus=0.6)
        ev = agg.aggregate((_m("x", "X", 0.8),))
        assert ev.score.final_score == 1.0
        assert any("plafonnement" in d.lower() for d in ev.explanation.details)

    def test_breakdown_sorted_by_metric_id(self) -> None:
        """Ordre du breakdown indépendant de l'ordre des métriques en entrée."""
        agg = WeightedScoreAggregator(
            weights={"zebra": 0.5, "alpha": 0.5},
        )
        ev = agg.aggregate(
            (
                _m("zebra", "Z", 0.2),
                _m("alpha", "A", 0.8),
            )
        )
        ids = [ln.metric_id for ln in ev.breakdown.lines]
        assert ids == ["alpha", "zebra"]

    def test_shares_sum_to_one(self) -> None:
        """Les parts de somme pondérée totalisent ~1."""
        agg = WeightedScoreAggregator(weights={"a": 0.25, "b": 0.75})
        ev = agg.aggregate(
            (
                _m("a", "A", 1.0),
                _m("b", "B", 0.5),
            )
        )
        total_share = sum(ln.share_of_weighted_sum for ln in ev.breakdown.lines)
        assert total_share == pytest.approx(1.0)

    def test_missing_weighted_metric_raises(self) -> None:
        """Métrique pondérée absente → erreur métier."""
        agg = WeightedScoreAggregator(weights={"a": 1.0})
        with pytest.raises(DeckEvaluationException, match="absente"):
            agg.aggregate(())

    def test_duplicate_metric_id_raises(self) -> None:
        """Duplication d'identifiant interdite."""
        agg = WeightedScoreAggregator(weights={"a": 0.5, "b": 0.5})
        with pytest.raises(DeckEvaluationException, match="dupliquée"):
            agg.aggregate(
                (
                    _m("a", "A1", 1.0),
                    _m("a", "A2", 0.0),
                    _m("b", "B", 0.5),
                )
            )

    def test_negative_weight_in_config_raises(self) -> None:
        """Poids négatif au constructeur."""
        with pytest.raises(DeckEvaluationException, match="négatif"):
            WeightedScoreAggregator(weights={"a": -0.1, "b": 1.0})

    def test_all_zero_weights_raises(self) -> None:
        """Somme nulle de poids actifs."""
        with pytest.raises(DeckEvaluationException, match="positif"):
            WeightedScoreAggregator(weights={"a": 0.0, "b": 0.0})

    def test_negative_default_penalty_raises(self) -> None:
        """Pénalité par défaut négative interdite au constructeur."""
        with pytest.raises(DeckEvaluationException, match="global_penalty"):
            WeightedScoreAggregator(weights={"x": 1.0}, global_penalty=-0.05)

    def test_explanation_readable(self) -> None:
        """Résumé et détails mentionnent bonus et lignes de métrique."""
        agg = WeightedScoreAggregator(
            weights={"only": 1.0},
            global_bonus=0.05,
            global_penalty=0.0,
        )
        ev = agg.aggregate((_m("only", "Only", 0.4),))
        assert "bonus" in ev.explanation.summary
        assert any("only" in d for d in ev.explanation.details)

    def test_extra_metric_ignored_in_breakdown(self) -> None:
        """Métrique hors table de poids : présente dans metrics, absente du breakdown."""
        agg = WeightedScoreAggregator(weights={"a": 1.0})
        ev = agg.aggregate(
            (
                _m("a", "A", 1.0),
                _m("extra", "E", 0.25),
            )
        )
        assert len(ev.breakdown.lines) == 1
        assert len(ev.metrics) == 2

    def test_aggregate_overrides_adjustments(self) -> None:
        """Surcharge bonus / pénalité sur aggregate."""
        agg = WeightedScoreAggregator(weights={"x": 1.0}, global_bonus=0.0, global_penalty=0.0)
        ev = agg.aggregate((_m("x", "X", 0.5),), global_bonus=0.2, global_penalty=0.1)
        assert ev.score.final_score == pytest.approx(0.6)

    def test_negative_adjustment_override_raises(self) -> None:
        """Bonus négatif interdit."""
        agg = WeightedScoreAggregator(weights={"x": 1.0})
        with pytest.raises(DeckEvaluationException, match="global_bonus"):
            agg.aggregate((_m("x", "X", 0.5),), global_bonus=-0.1)

    def test_default_weights_all_five_metrics(self) -> None:
        """Agrégateur par défaut avec les cinq ``metric_id`` standard."""
        agg = WeightedScoreAggregator()
        metrics = tuple(_m(mid, mid, 0.4) for mid in sorted(default_metric_weights().keys()))
        ev = agg.aggregate(metrics)
        assert ev.score.weighted_average == pytest.approx(0.4)
        assert len(ev.breakdown.lines) == 5
