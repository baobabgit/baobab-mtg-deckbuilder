"""Règle exécutable de validation sur un deck."""

from __future__ import annotations

from abc import ABC, abstractmethod

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue


class DeckValidationRule(ABC):
    """Contrat des règles appliquées par un :class:`FormatDefinition`.

    Chaque règle est stateless vis-à-vis du deck ; elle peut porter des paramètres
    de format en attributs d'instance (seuils, listes de référence).
    """

    @property
    @abstractmethod
    def rule_id(self) -> str:
        """Identifiant stable de la règle (ex. ``constructed.main_min_60``)."""

    @abstractmethod
    def evaluate(self, deck: Deck) -> tuple[DeckValidationIssue, ...]:
        """Évalue le deck et retourne zéro, une ou plusieurs issues."""
