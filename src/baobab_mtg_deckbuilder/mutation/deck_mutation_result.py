"""Résultat structuré d'une mutation : avant / après, validation et impact."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.mutation.deck_mutation import DeckMutation
from baobab_mtg_deckbuilder.validation.deck_validation_report import DeckValidationReport

MutationImpact: TypeAlias = Literal["beneficial", "neutral", "degrading"]


@dataclass(frozen=True, slots=True)
class DeckMutationResult:
    """Sortie d'un :class:`DeckMutationOperator`.

    :param operator_id: Identifiant de l'opérateur ayant produit ce résultat.
    :type operator_id: str
    :param deck_before: Deck d'entrée.
    :type deck_before: Deck
    :param deck_after: Deck après application (immuables distincts).
    :type deck_after: Deck
    :param mutations_applied: Journal des mutations unitaires.
    :type mutations_applied: tuple[DeckMutation, ...]
    :param justification: Synthèse métier de l'intention / du mécanisme.
    :type justification: str
    :param validation_report_before: Rapport de validation sur ``deck_before``.
    :type validation_report_before: DeckValidationReport
    :param validation_report_after: Rapport de validation sur ``deck_after``.
    :type validation_report_after: DeckValidationReport
    :param impact: Impact heuristique dérivé d'un score optionnel ou neutre par défaut.
    :type impact: MutationImpact
    """

    operator_id: str
    deck_before: Deck
    deck_after: Deck
    mutations_applied: tuple[DeckMutation, ...]
    justification: str
    validation_report_before: DeckValidationReport
    validation_report_after: DeckValidationReport
    impact: MutationImpact
