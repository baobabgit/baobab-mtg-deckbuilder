"""Tests for :class:`DeckMetric`."""

from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)
from baobab_mtg_deckbuilder.evaluation.deck_metric import DeckMetric


class TestDeckMetric:
    """Value object for metric results."""

    def test_fields(self) -> None:
        """All public fields are accessible."""
        explanation = DeckEvaluationExplanation(
            title="T",
            summary="S",
            details=("d1",),
        )
        metric = DeckMetric(
            metric_id="m1",
            display_name="M",
            raw_score=42.5,
            normalized_score=0.42,
            explanation=explanation,
        )
        assert metric.metric_id == "m1"
        assert metric.explanation.summary == "S"
