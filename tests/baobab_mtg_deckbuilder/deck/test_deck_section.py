"""Tests for :class:`DeckSection`."""

import pytest

from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import (
    MAIN_DECK_SECTION_ID,
    SIDEBOARD_SECTION_ID,
    DeckSection,
)
from baobab_mtg_deckbuilder.exceptions.deck_validation_exception import (
    DeckValidationException,
)


class TestDeckSection:
    """Tests for main and sideboard sections."""

    def test_main_factory_sets_identifier(self) -> None:
        """``DeckSection.main`` tags the standard main id."""
        section = DeckSection.main([DeckCardEntry("Island", 10)])
        assert section.identifier == MAIN_DECK_SECTION_ID

    def test_sideboard_factory_sets_identifier(self) -> None:
        """``DeckSection.sideboard`` tags the standard sideboard id."""
        section = DeckSection.sideboard([])
        assert section.identifier == SIDEBOARD_SECTION_ID

    def test_total_quantity_sums_entries(self) -> None:
        """``total_quantity`` sums all line quantities."""
        section = DeckSection.main(
            [
                DeckCardEntry("A", 2),
                DeckCardEntry("B", 3),
            ]
        )
        assert section.total_quantity == 5

    def test_empty_sideboard_allowed(self) -> None:
        """Limited or pre-sideboard lists may have zero sideboard lines."""
        section = DeckSection.sideboard([])
        assert section.entries == ()
        assert section.total_quantity == 0

    def test_rejects_blank_identifier(self) -> None:
        """Empty section id raises :class:`DeckValidationException`."""
        with pytest.raises(DeckValidationException):
            DeckSection("  ", (DeckCardEntry("X", 1),))
