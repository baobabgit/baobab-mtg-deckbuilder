"""Format factice pour couvrir les branches « non supporté » (tests uniquement)."""

from __future__ import annotations

from baobab_mtg_deckbuilder.validation.deck_constraint_set import DeckConstraintSet
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule
from baobab_mtg_deckbuilder.validation.format_definition import FormatDefinition


class UnsupportedFormatDefinitionForTests(FormatDefinition):
    """Format minimal hors MVP Construit / Limité."""

    @property
    def format_key(self) -> str:
        return "unsupported_test_only"

    def constraint_set(self) -> DeckConstraintSet:
        return DeckConstraintSet(format_key=self.format_key, constraints=())

    def validation_rules(self) -> tuple[DeckValidationRule, ...]:
        return ()
