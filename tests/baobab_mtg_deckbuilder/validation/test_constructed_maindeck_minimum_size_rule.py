"""Tests for :class:`ConstructedMaindeckMinimumSizeRule`."""

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.validation.constructed_maindeck_minimum_size_rule import (
    ConstructedMaindeckMinimumSizeRule,
)
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)


class TestConstructedMaindeckMinimumSizeRule:
    """Unit tests for main deck minimum size."""

    def test_rule_id_stable(self) -> None:
        """Rule id is documented and stable."""
        assert ConstructedMaindeckMinimumSizeRule(60).rule_id == "constructed.maindeck_minimum_size"

    def test_passes_at_threshold(self) -> None:
        """Exactly minimum cards passes."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Swamp", 60)]),
            DeckSection.sideboard([]),
        )
        issues = ConstructedMaindeckMinimumSizeRule(60).evaluate(deck)
        assert issues == ()

    def test_fails_below_threshold(self) -> None:
        """Below minimum yields an error with suggestion."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Swamp", 59)]),
            DeckSection.sideboard([]),
        )
        issues = ConstructedMaindeckMinimumSizeRule(60).evaluate(deck)
        assert len(issues) == 1
        assert issues[0].severity == DeckValidationIssueSeverity.ERROR
        assert issues[0].suggestion is not None
