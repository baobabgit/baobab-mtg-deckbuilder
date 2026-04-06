"""Règle : taille maximale du sideboard (Construit)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule


@dataclass(frozen=True, slots=True)
class ConstructedSideboardMaximumSizeRule(DeckValidationRule):
    """Vérifie que le sideboard ne dépasse pas ``maximum_cards`` cartes."""

    maximum_cards: int

    @property
    def rule_id(self) -> str:
        return "constructed.sideboard_maximum_size"

    def evaluate(self, deck: Deck) -> tuple[DeckValidationIssue, ...]:
        total = deck.sideboard_total_quantity
        if total <= self.maximum_cards:
            return ()
        over = total - self.maximum_cards
        return (
            DeckValidationIssue(
                severity=DeckValidationIssueSeverity.ERROR,
                code="CONSTRUCTED_SIDEBOARD_TOO_LARGE",
                message=(
                    f"Le sideboard contient {total} carte(s), "
                    f"au plus {self.maximum_cards} sont autorisées."
                ),
                affected_entity="sideboard",
                suggestion=f"Retirer au moins {over} carte(s) du sideboard.",
            ),
        )
