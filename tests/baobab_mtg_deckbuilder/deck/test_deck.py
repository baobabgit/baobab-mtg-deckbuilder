"""Tests for :class:`Deck`."""

import pytest

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.exceptions.deck_validation_exception import (
    DeckValidationException,
)


class TestDeck:
    """Integration tests for full deck model (constructed / limited style)."""

    def test_valid_constructed_style_deck(self) -> None:
        """A typical main + sideboard deck builds without error."""
        main = DeckSection.main(
            [
                DeckCardEntry("Delver of Secrets", 4),
                DeckCardEntry("Lightning Bolt", 4),
            ]
        )
        side = DeckSection.sideboard([DeckCardEntry("Pyroblast", 2)])
        deck = Deck.from_sections(main, side)
        assert deck.main_total_quantity == 8
        assert deck.sideboard_total_quantity == 2
        assert deck.total_quantity == 10

    def test_limited_empty_sideboard(self) -> None:
        """Limited lists often register an empty sideboard section."""
        main = DeckSection.main([DeckCardEntry("Forest", 8), DeckCardEntry("Balduvian Bears", 1)])
        side = DeckSection.sideboard([])
        deck = Deck.from_sections(main, side)
        assert deck.main_total_quantity == 9
        assert deck.sideboard_total_quantity == 0

    def test_list_view_sorts_independently_of_insertion_order(self) -> None:
        """``list_view`` exposes deterministic ordering."""
        main = DeckSection.main(
            [
                DeckCardEntry("Zombie", 1),
                DeckCardEntry("Abrade", 2),
            ]
        )
        deck = Deck.from_sections(main, DeckSection.sideboard([]))
        view = deck.list_view()
        assert [e.english_name for e in view.main_entries] == ["Abrade", "Zombie"]

    def test_summary_counts_by_english_name(self) -> None:
        """``summary`` groups quantities by normalized English oracle name."""
        deck = Deck.from_sections(
            DeckSection.main(
                [
                    DeckCardEntry("Counterspell", 2),
                    DeckCardEntry("Counterspell", 2),
                ]
            ),
            DeckSection.sideboard([]),
        )
        s = deck.summary()
        assert s.main_quantity_by_english_name["Counterspell"] == 4

    def test_rejects_swapped_sections(self) -> None:
        """Main section id must be ``main``, sideboard must be ``sideboard``."""
        main = DeckSection.sideboard([])
        side = DeckSection.main([])
        with pytest.raises(DeckValidationException):
            Deck.from_sections(main, side)

    def test_rejects_custom_section_as_main(self) -> None:
        """A non-main identifier cannot be used as ``main_section``."""
        wrong = DeckSection("commander", (DeckCardEntry("Sol Ring", 1),))
        side = DeckSection.sideboard([])
        with pytest.raises(DeckValidationException):
            Deck.from_sections(wrong, side)

    def test_rejects_wrong_sideboard_identifier(self) -> None:
        """The sideboard section must use the standard ``sideboard`` id."""
        main = DeckSection.main([DeckCardEntry("Grizzly Bears", 1)])
        bad_side = DeckSection("side", ())
        with pytest.raises(DeckValidationException):
            Deck.from_sections(main, bad_side)
