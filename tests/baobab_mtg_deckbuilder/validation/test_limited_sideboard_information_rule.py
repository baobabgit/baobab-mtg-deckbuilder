"""Tests for :class:`LimitedSideboardInformationRule`."""

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)
from baobab_mtg_deckbuilder.validation.limited_sideboard_information_rule import (
    LimitedSideboardInformationRule,
)


class TestLimitedSideboardInformationRule:
    """Unit tests for sideboard info in limited."""

    def test_rule_id_stable(self) -> None:
        """Rule id is documented and stable."""
        assert LimitedSideboardInformationRule().rule_id == "limited.sideboard_information"

    def test_empty_sideboard_silent(self) -> None:
        """No issue when sideboard empty."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Island", 40)]),
            DeckSection.sideboard([]),
        )
        assert LimitedSideboardInformationRule().evaluate(deck) == ()

    def test_nonempty_emits_info(self) -> None:
        """Non-empty sideboard emits info."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Island", 40)]),
            DeckSection.sideboard([DeckCardEntry("Dispel", 1)]),
        )
        issues = LimitedSideboardInformationRule().evaluate(deck)
        assert len(issues) == 1
        assert issues[0].severity == DeckValidationIssueSeverity.INFO
