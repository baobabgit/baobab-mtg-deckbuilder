"""Tests for :class:`LimitedMaindeckMinimumSizeRule`."""

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.validation.limited_maindeck_minimum_size_rule import (
    LimitedMaindeckMinimumSizeRule,
)


class TestLimitedMaindeckMinimumSizeRule:
    """Unit tests for limited main minimum."""

    def test_rule_id_stable(self) -> None:
        """Rule id is documented and stable."""
        assert LimitedMaindeckMinimumSizeRule(40).rule_id == "limited.maindeck_minimum_size"

    def test_passes_at_forty(self) -> None:
        """40 cards is enough."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Forest", 40)]),
            DeckSection.sideboard([]),
        )
        assert LimitedMaindeckMinimumSizeRule(40).evaluate(deck) == ()

    def test_fails_at_thirty_nine(self) -> None:
        """39 cards fails."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Forest", 39)]),
            DeckSection.sideboard([]),
        )
        issues = LimitedMaindeckMinimumSizeRule(40).evaluate(deck)
        assert len(issues) == 1
