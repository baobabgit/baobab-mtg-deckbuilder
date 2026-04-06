"""Avertissement si le sideboard limité dépasse un seuil de référence."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule


@dataclass(frozen=True, slots=True)
class LimitedSideboardSizeWarningRule(DeckValidationRule):
    """Émet un avertissement lorsque le sideboard dépasse ``recommended_maximum``.

    Le seuil reprend la borne usuelle du construit à titre indicatif pour le
    limité (soumission deck / cartes hors jeu actif).

    :param recommended_maximum: Seuil déclenchant l'avertissement (défaut 15).
    :type recommended_maximum: int
    """

    recommended_maximum: int = 15

    @property
    def rule_id(self) -> str:
        return "limited.sideboard_size_warning"

    def evaluate(self, deck: Deck) -> tuple[DeckValidationIssue, ...]:
        total = deck.sideboard_total_quantity
        if total <= self.recommended_maximum:
            return ()
        return (
            DeckValidationIssue(
                severity=DeckValidationIssueSeverity.WARNING,
                code="LIMITED_SIDEBOARD_LARGE",
                message=(
                    f"Le sideboard contient {total} carte(s), "
                    f"au-delà du repère courant de {self.recommended_maximum} cartes."
                ),
                affected_entity="sideboard",
                suggestion="Vérifier le nombre de cartes hors main autorisé pour l'évènement.",
            ),
        )
