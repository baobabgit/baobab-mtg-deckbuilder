"""Tests for :class:`DeckConstraintSet`."""

from baobab_mtg_deckbuilder.validation.deck_constraint import DeckConstraint
from baobab_mtg_deckbuilder.validation.deck_constraint_set import DeckConstraintSet


class TestDeckConstraintSet:
    """Tests for grouped constraints."""

    def test_holds_format_key_and_constraints(self) -> None:
        """Format key and tuple are stored."""
        inner = (DeckConstraint("A", "one"),)
        cs = DeckConstraintSet(format_key="fmt", constraints=inner)
        assert cs.format_key == "fmt"
        assert cs.constraints == inner
