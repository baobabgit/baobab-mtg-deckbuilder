"""Tests for :class:`ConstructedFormatDefinition` (MVP rules)."""

import pytest

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.exceptions.deck_configuration_exception import (
    DeckConfigurationException,
)
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)


def _sixty_basic_main() -> DeckSection:
    return DeckSection.main([DeckCardEntry("Forest", 60)])


def _valid_constructed_sideboard() -> DeckSection:
    return DeckSection.sideboard([DeckCardEntry("Naturalize", 15)])


class TestConstructedFormatDefinition:
    """Integration tests for constructed MVP validation."""

    def test_valid_constructed_deck(self) -> None:
        """60-card main, legal sideboard, max 4 non-basics."""
        main = DeckSection.main(
            [DeckCardEntry("Lightning Bolt", 4)] + [DeckCardEntry("Mountain", 56)]
        )
        side = _valid_constructed_sideboard()
        deck = Deck.from_sections(main, side)
        fmt = ConstructedFormatDefinition()
        report = fmt.validate(deck)
        assert report.is_valid
        assert report.error_count == 0

    def test_invalid_main_too_small(self) -> None:
        """Fewer than 60 cards in main is an error."""
        main = DeckSection.main([DeckCardEntry("Island", 59)])
        deck = Deck.from_sections(main, DeckSection.sideboard([]))
        report = ConstructedFormatDefinition().validate(deck)
        assert report.is_valid is False
        assert any(i.code == "CONSTRUCTED_MAIN_TOO_SMALL" for i in report.issues)

    def test_invalid_too_many_copies_nonbasic(self) -> None:
        """More than 4 copies of the same non-basic name fails."""
        main = DeckSection.main([DeckCardEntry("Dark Ritual", 5)] + [DeckCardEntry("Swamp", 55)])
        deck = Deck.from_sections(main, DeckSection.sideboard([]))
        report = ConstructedFormatDefinition().validate(deck)
        assert report.is_valid is False
        assert any(i.code == "CONSTRUCTED_TOO_MANY_COPIES" for i in report.issues)
        too_many = next(i for i in report.issues if i.code == "CONSTRUCTED_TOO_MANY_COPIES")
        assert too_many.affected_entity == "Dark Ritual"
        assert too_many.suggestion is not None

    def test_basic_lands_ignore_four_copy_rule(self) -> None:
        """More than 4 Forest is allowed."""
        main = _sixty_basic_main()
        deck = Deck.from_sections(main, DeckSection.sideboard([]))
        report = ConstructedFormatDefinition().validate(deck)
        assert report.is_valid

    def test_invalid_sideboard_too_large(self) -> None:
        """More than 15 sideboard cards is an error."""
        main = _sixty_basic_main()
        side = DeckSection.sideboard([DeckCardEntry("Goblin", 16)])
        deck = Deck.from_sections(main, side)
        report = ConstructedFormatDefinition().validate(deck)
        assert any(i.code == "CONSTRUCTED_SIDEBOARD_TOO_LARGE" for i in report.issues)

    def test_constraint_set_documents_rules(self) -> None:
        """Constraint set exposes MVP parameters."""
        fmt = ConstructedFormatDefinition()
        cs = fmt.constraint_set()
        assert cs.format_key == "constructed_mvp"
        codes = {c.code for c in cs.constraints}
        assert "CONSTRUCTED_MAIN_MIN" in codes
        assert "CONSTRUCTED_NONBASIC_MAX_COPIES" in codes
        assert "CONSTRUCTED_SIDEBOARD_MAX" in codes

    def test_rejects_invalid_configuration(self) -> None:
        """Non-positive thresholds raise :class:`DeckConfigurationException`."""
        with pytest.raises(DeckConfigurationException):
            ConstructedFormatDefinition(main_minimum_cards=0)

    def test_rejects_negative_sideboard_cap(self) -> None:
        """Negative sideboard maximum is rejected."""
        with pytest.raises(DeckConfigurationException):
            ConstructedFormatDefinition(sideboard_maximum_cards=-1)

    def test_rejects_non_positive_max_copies(self) -> None:
        """Max copies rule must allow at least one copy."""
        with pytest.raises(DeckConfigurationException):
            ConstructedFormatDefinition(max_copies_excluding_basic_lands=0)
