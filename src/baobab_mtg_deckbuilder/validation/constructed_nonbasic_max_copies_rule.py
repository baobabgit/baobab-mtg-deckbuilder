"""Règle : exemplaires max par carte non-terrain de base (Construit)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)
from baobab_mtg_deckbuilder.validation.deck_validation_rule import DeckValidationRule


@dataclass(frozen=True, slots=True)
class ConstructedNonbasicMaxCopiesRule(DeckValidationRule):
    """Limite le nombre d'exemplaires par nom Oracle hors terrains de base."""

    basic_land_oracle_names: frozenset[str]
    max_copies: int

    @property
    def rule_id(self) -> str:
        return "constructed.nonbasic_max_copies"

    def evaluate(self, deck: Deck) -> tuple[DeckValidationIssue, ...]:
        counts: dict[str, int] = {}
        for entry in deck.main_section.entries:
            counts[entry.english_name] = counts.get(entry.english_name, 0) + entry.quantity
        issues: list[DeckValidationIssue] = []
        for name, qty in sorted(counts.items(), key=lambda x: (x[0].lower(), x[0])):
            if name in self.basic_land_oracle_names:
                continue
            if qty <= self.max_copies:
                continue
            over = qty - self.max_copies
            issues.append(
                DeckValidationIssue(
                    severity=DeckValidationIssueSeverity.ERROR,
                    code="CONSTRUCTED_TOO_MANY_COPIES",
                    message=(
                        f"La carte « {name} » apparaît {qty} fois dans le main "
                        f"(maximum {self.max_copies} hors terrains de base)."
                    ),
                    affected_entity=name,
                    suggestion=(
                        f"Retirer au moins {over} exemplaire(s) de « {name} » du main deck."
                    ),
                )
            )
        return tuple(issues)
