"""Tests for :class:`DeckScore`."""

from baobab_mtg_deckbuilder.evaluation.deck_score import DeckScore


class TestDeckScore:
    """Value object."""

    def test_fields(self) -> None:
        """Accès aux champs."""
        s = DeckScore(
            weighted_average=0.7,
            global_bonus=0.05,
            global_penalty=0.1,
            final_score=0.65,
            total_weight=2.5,
        )
        assert s.final_score == 0.65
        assert s.total_weight == 2.5
