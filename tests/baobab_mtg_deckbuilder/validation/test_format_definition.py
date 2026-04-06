"""Tests for :class:`FormatDefinition`."""

from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.validation.deck_constraint import DeckConstraint
from baobab_mtg_deckbuilder.validation.deck_constraint_set import DeckConstraintSet
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule
from baobab_mtg_deckbuilder.validation.format_definition import FormatDefinition
from tests.baobab_mtg_deckbuilder.validation.always_error_validation_rule import (
    AlwaysErrorValidationRule,
)


@dataclass(frozen=True, slots=True)
class _TinyFormat(FormatDefinition):
    """Minimal format wiring one rule for ``validate``."""

    @property
    def format_key(self) -> str:
        return "tiny_test"

    def constraint_set(self) -> DeckConstraintSet:
        return DeckConstraintSet(
            format_key=self.format_key,
            constraints=(DeckConstraint("C", "constraint"),),
        )

    def validation_rules(self) -> tuple[DeckValidationRule, ...]:
        return (AlwaysErrorValidationRule(),)


class TestFormatDefinition:
    """Tests for abstract format orchestration."""

    def test_validate_runs_all_rules(self) -> None:
        """validate aggregates rule issues into a report."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Island", 60)]),
            DeckSection.sideboard([]),
        )
        fmt: FormatDefinition = _TinyFormat()
        report = fmt.validate(deck)
        assert report.error_count == 1
        assert report.issues[0].code == "TEST"
