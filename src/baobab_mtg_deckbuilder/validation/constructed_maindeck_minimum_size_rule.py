"""Règle : nombre minimal de cartes dans le main (Construit)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule
from baobab_mtg_deckbuilder.validation.maindeck_minimum_support import (
    issues_when_main_below_minimum,
)


@dataclass(frozen=True, slots=True)
class ConstructedMaindeckMinimumSizeRule(DeckValidationRule):
    """Vérifie que le main contient au moins ``minimum_cards`` cartes."""

    minimum_cards: int

    @property
    def rule_id(self) -> str:
        return "constructed.maindeck_minimum_size"

    def evaluate(self, deck: Deck) -> tuple[DeckValidationIssue, ...]:
        total = deck.main_total_quantity
        missing = self.minimum_cards - total
        return issues_when_main_below_minimum(
            total,
            self.minimum_cards,
            error_code="CONSTRUCTED_MAIN_TOO_SMALL",
            message=(
                f"Le main deck contient {total} carte(s), "
                f"au moins {self.minimum_cards} sont requises pour ce format."
            ),
            suggestion=(f"Ajouter au moins {missing} carte(s) dans le main deck (hors sideboard)."),
        )
