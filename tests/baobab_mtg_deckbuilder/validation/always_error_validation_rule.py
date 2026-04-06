"""Règle de test toujours en erreur (partagée entre tests du package validation)."""

from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule


@dataclass(frozen=True, slots=True)
class AlwaysErrorValidationRule(DeckValidationRule):
    """Émet une erreur fixe pour vérifier l'orchestration des formats."""

    @property
    def rule_id(self) -> str:
        return "test.always_error"

    def evaluate(self, _deck: Deck) -> tuple[DeckValidationIssue, ...]:
        return (
            DeckValidationIssue(
                severity=DeckValidationIssueSeverity.ERROR,
                code="TEST",
                message="fail",
                affected_entity="deck",
                suggestion="fix",
            ),
        )
