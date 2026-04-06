"""Tests for :class:`DeckEvaluation`."""

from baobab_mtg_deckbuilder.evaluation.deck_evaluation import DeckEvaluation
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_breakdown import DeckEvaluationBreakdown
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_breakdown_line import (
    DeckEvaluationBreakdownLine,
)
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)
from baobab_mtg_deckbuilder.evaluation.deck_metric import DeckMetric
from baobab_mtg_deckbuilder.evaluation.deck_score import DeckScore


class TestDeckEvaluation:
    """Bundle complet."""

    def test_holds_parts(self) -> None:
        """Références cohérentes."""
        metric = DeckMetric(
            metric_id="x",
            display_name="X",
            raw_score=1.0,
            normalized_score=1.0,
            explanation=DeckEvaluationExplanation("t", "s", ()),
        )
        line = DeckEvaluationBreakdownLine(
            metric_id="x",
            display_name="X",
            weight=1.0,
            normalized_score=1.0,
            weighted_product=1.0,
            share_of_weighted_sum=1.0,
        )
        bd = DeckEvaluationBreakdown(
            lines=(line,),
            total_weight=1.0,
            weighted_sum=1.0,
            weighted_average=1.0,
        )
        sc = DeckScore(
            weighted_average=1.0,
            global_bonus=0.0,
            global_penalty=0.0,
            final_score=1.0,
            total_weight=1.0,
        )
        exp = DeckEvaluationExplanation("T", "S", ())
        ev = DeckEvaluation(metrics=(metric,), score=sc, breakdown=bd, explanation=exp)
        assert ev.score.final_score == 1.0
        assert len(ev.breakdown.lines) == 1
