"""Tests for :class:`LimitedFormatDefinition` (MVP rules)."""

import pytest

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.exceptions.deck_configuration_exception import (
    DeckConfigurationException,
)
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)
from baobab_mtg_deckbuilder.validation.limited_format_definition import (
    LimitedFormatDefinition,
)


class TestLimitedFormatDefinition:
    """Integration tests for limited MVP validation."""

    def test_valid_limited_deck(self) -> None:
        """40-card main satisfies the minimum."""
        main = DeckSection.main([DeckCardEntry("Forest", 40)])
        deck = Deck.from_sections(main, DeckSection.sideboard([]))
        report = LimitedFormatDefinition().validate(deck)
        assert report.is_valid
        assert report.error_count == 0

    def test_invalid_main_too_small(self) -> None:
        """Fewer than 40 main cards is an error."""
        main = DeckSection.main([DeckCardEntry("Plains", 39)])
        deck = Deck.from_sections(main, DeckSection.sideboard([]))
        report = LimitedFormatDefinition().validate(deck)
        assert report.is_valid is False
        assert any(i.code == "LIMITED_MAIN_TOO_SMALL" for i in report.issues)

    def test_sideboard_emits_info(self) -> None:
        """Non-empty sideboard produces an informational issue."""
        main = DeckSection.main([DeckCardEntry("Mountain", 40)])
        side = DeckSection.sideboard([DeckCardEntry("Lava Spike", 1)])
        deck = Deck.from_sections(main, side)
        report = LimitedFormatDefinition().validate(deck)
        assert report.is_valid
        infos = [i for i in report.issues if i.severity == DeckValidationIssueSeverity.INFO]
        assert any(i.code == "LIMITED_SIDEBOARD_PRESENT" for i in infos)

    def test_large_sideboard_emits_warning(self) -> None:
        """Sideboard above the soft threshold yields a warning."""
        main = DeckSection.main([DeckCardEntry("Island", 40)])
        side = DeckSection.sideboard([DeckCardEntry("Negate", 16)])
        deck = Deck.from_sections(main, side)
        report = LimitedFormatDefinition().validate(deck)
        assert report.is_valid
        warnings = [i for i in report.issues if i.severity == DeckValidationIssueSeverity.WARNING]
        assert any(i.code == "LIMITED_SIDEBOARD_LARGE" for i in warnings)

    def test_rejects_invalid_configuration(self) -> None:
        """Invalid minimum main size raises :class:`DeckConfigurationException`."""
        with pytest.raises(DeckConfigurationException):
            LimitedFormatDefinition(main_minimum_cards=0)

    def test_constraint_set_exposes_format_key(self) -> None:
        """Declarative constraints reference the limited format key."""
        fmt = LimitedFormatDefinition()
        cs = fmt.constraint_set()
        assert cs.format_key == "limited_mvp"
        assert len(cs.constraints) == 1
        assert cs.constraints[0].code == "LIMITED_MAIN_MIN"
