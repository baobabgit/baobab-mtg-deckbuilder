"""Tests for :class:`DeckConstraint`."""

from baobab_mtg_deckbuilder.validation.deck_constraint import DeckConstraint


class TestDeckConstraint:
    """Tests for declarative constraints."""

    def test_optional_value(self) -> None:
        """Value may be omitted."""
        c = DeckConstraint(code="X", summary="desc")
        assert c.value is None

    def test_with_value(self) -> None:
        """Integer value is preserved."""
        c = DeckConstraint(code="MIN", summary="min cards", value=60)
        assert c.value == 60
