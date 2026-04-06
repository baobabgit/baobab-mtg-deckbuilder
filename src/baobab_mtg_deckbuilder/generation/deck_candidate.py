"""Candidat de deck issu d'une stratégie de génération."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.validation.deck_validation_report import DeckValidationReport


@dataclass(frozen=True, slots=True)
class DeckCandidate:
    """Un deck proposé, avec le rapport de validation du format demandé.

    :param candidate_index: Indice stable du candidat dans la série (0-based).
    :type candidate_index: int
    :param deck: Deck construit (main rempli, sideboard souvent vide à ce stade).
    :type deck: Deck
    :param validation_report: Résultat de :meth:`FormatDefinition.validate`.
    :type validation_report: DeckValidationReport
    """

    candidate_index: int
    deck: Deck
    validation_report: DeckValidationReport

    @property
    def is_valid(self) -> bool:
        """Vrai si le rapport ne contient aucune erreur bloquante."""
        return self.validation_report.is_valid
