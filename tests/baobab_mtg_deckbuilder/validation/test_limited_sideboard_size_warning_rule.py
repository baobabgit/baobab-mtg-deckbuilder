"""Tests for :class:`LimitedSideboardSizeWarningRule`."""

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)
from baobab_mtg_deckbuilder.validation.limited_sideboard_size_warning_rule import (
    LimitedSideboardSizeWarningRule,
)


class TestLimitedSideboardSizeWarningRule:
    """Unit tests for soft sideboard size warning."""

    def test_rule_id_stable(self) -> None:
        """Rule id is documented and stable."""
        assert LimitedSideboardSizeWarningRule(15).rule_id == "limited.sideboard_size_warning"

    def test_no_warning_when_small(self) -> None:
        """Up to threshold is silent."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Mountain", 40)]),
            DeckSection.sideboard([DeckCardEntry("Smash", 15)]),
        )
        assert LimitedSideboardSizeWarningRule(15).evaluate(deck) == ()

    def test_warning_when_above_threshold(self) -> None:
        """Above threshold warns."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Mountain", 40)]),
            DeckSection.sideboard([DeckCardEntry("Smash", 16)]),
        )
        issues = LimitedSideboardSizeWarningRule(15).evaluate(deck)
        assert len(issues) == 1
        assert issues[0].severity == DeckValidationIssueSeverity.WARNING
