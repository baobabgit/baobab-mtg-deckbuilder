"""Règle informative : présence d'un sideboard en contexte limité."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule


@dataclass(frozen=True, slots=True)
class LimitedSideboardInformationRule(DeckValidationRule):
    """Émet une info si le sideboard n'est pas vide (rappel réglementaire)."""

    @property
    def rule_id(self) -> str:
        return "limited.sideboard_information"

    def evaluate(self, deck: Deck) -> tuple[DeckValidationIssue, ...]:
        total = deck.sideboard_total_quantity
        if total == 0:
            return ()
        return (
            DeckValidationIssue(
                severity=DeckValidationIssueSeverity.INFO,
                code="LIMITED_SIDEBOARD_PRESENT",
                message=(
                    f"Le sideboard contient {total} carte(s). "
                    "Vérifiez le réglement du tournoi (deck limité vs cartes hors deck)."
                ),
                affected_entity="sideboard",
                suggestion=None,
            ),
        )
