"""Tests for :class:`CardPoolEntry`."""

import pytest

from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry
from baobab_mtg_deckbuilder.exceptions.deck_validation_exception import (
    DeckValidationException,
)


class TestCardPoolEntry:
    """Tests for pool lines."""

    def test_strips_oracle_name(self) -> None:
        """Oracle name is normalized."""
        entry = CardPoolEntry("  Shock  ", None)
        assert entry.english_oracle_name == "Shock"

    def test_unbounded_quantity(self) -> None:
        """None marks unbounded availability in a theoretical sense."""
        entry = CardPoolEntry("Forest", None)
        assert entry.available_quantity is None

    def test_bounded_quantity(self) -> None:
        """Integer quantities are preserved."""
        entry = CardPoolEntry("Island", 3)
        assert entry.available_quantity == 3

    def test_rejects_empty_name(self) -> None:
        """Blank oracle name raises."""
        with pytest.raises(DeckValidationException):
            CardPoolEntry("  ", 1)

    def test_rejects_negative_quantity(self) -> None:
        """Negative bounded quantity raises."""
        with pytest.raises(DeckValidationException):
            CardPoolEntry("Swamp", -1)
