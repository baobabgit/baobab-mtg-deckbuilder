"""Tests for :class:`ConstructedSideboardMaximumSizeRule`."""

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.validation.constructed_sideboard_maximum_size_rule import (
    ConstructedSideboardMaximumSizeRule,
)


class TestConstructedSideboardMaximumSizeRule:
    """Unit tests for sideboard cap."""

    def test_rule_id_stable(self) -> None:
        """Rule id is documented and stable."""
        assert (
            ConstructedSideboardMaximumSizeRule(15).rule_id == "constructed.sideboard_maximum_size"
        )

    def test_allows_fifteen(self) -> None:
        """15 sideboard cards pass."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Plains", 60)]),
            DeckSection.sideboard([DeckCardEntry("Erase", 15)]),
        )
        assert ConstructedSideboardMaximumSizeRule(15).evaluate(deck) == ()

    def test_rejects_sixteen(self) -> None:
        """16 sideboard cards fail."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Plains", 60)]),
            DeckSection.sideboard([DeckCardEntry("Erase", 16)]),
        )
        issues = ConstructedSideboardMaximumSizeRule(15).evaluate(deck)
        assert len(issues) == 1
