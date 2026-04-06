"""Tests for :class:`DeckEvaluationExplanation`."""

from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)


class TestDeckEvaluationExplanation:
    """Structured explanation lines."""

    def test_immutable_details_tuple(self) -> None:
        """Details are stored as tuple."""
        exp = DeckEvaluationExplanation(
            title="a",
            summary="b",
            details=("x", "y"),
        )
        assert exp.details == ("x", "y")
