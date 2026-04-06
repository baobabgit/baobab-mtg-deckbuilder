"""Tests for :class:`DeckEvaluationBreakdownLine`."""

from baobab_mtg_deckbuilder.evaluation.deck_evaluation_breakdown_line import (
    DeckEvaluationBreakdownLine,
)


class TestDeckEvaluationBreakdownLine:
    """Ligne de breakdown."""

    def test_immutable_row(self) -> None:
        """Frozen dataclass."""
        ln = DeckEvaluationBreakdownLine(
            metric_id="m",
            display_name="M",
            weight=0.5,
            normalized_score=0.8,
            weighted_product=0.4,
            share_of_weighted_sum=1.0,
        )
        assert ln.weighted_product == 0.4
