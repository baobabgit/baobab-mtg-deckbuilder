"""Tests for :class:`DeckValidationRule`."""

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule
from tests.baobab_mtg_deckbuilder.validation.always_error_validation_rule import (
    AlwaysErrorValidationRule,
)


class TestDeckValidationRule:
    """Smoke tests for the rule protocol."""

    def test_evaluate_returns_issues(self) -> None:
        """Concrete rule produces issues."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Forest", 1)]),
            DeckSection.sideboard([]),
        )
        rule: DeckValidationRule = AlwaysErrorValidationRule()
        issues = rule.evaluate(deck)
        assert len(issues) == 1
        assert issues[0].code == "TEST"
