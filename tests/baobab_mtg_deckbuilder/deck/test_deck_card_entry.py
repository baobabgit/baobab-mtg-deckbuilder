"""Tests for :class:`DeckCardEntry`."""

import pytest

from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.exceptions.deck_validation_exception import (
    DeckValidationException,
)


class TestDeckCardEntry:
    """Tests for deck line entries."""

    def test_strips_english_name(self) -> None:
        """Leading and trailing spaces are stripped from the oracle name."""
        entry = DeckCardEntry("  Lightning Bolt  ", 4)
        assert entry.english_name == "Lightning Bolt"

    def test_valid_quantity(self) -> None:
        """Quantity 1 is accepted."""
        entry = DeckCardEntry("Forest", 1)
        assert entry.quantity == 1

    def test_rejects_empty_name(self) -> None:
        """Blank oracle name raises :class:`DeckValidationException`."""
        with pytest.raises(DeckValidationException):
            DeckCardEntry("   ", 1)

    def test_rejects_zero_quantity(self) -> None:
        """Non-positive quantity raises :class:`DeckValidationException`."""
        with pytest.raises(DeckValidationException):
            DeckCardEntry("Swamp", 0)
