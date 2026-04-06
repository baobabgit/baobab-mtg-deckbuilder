"""Contrat des opérateurs de mutation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.mutation.deck_mutation_result import DeckMutationResult


class DeckMutationOperator(ABC):
    """Transforme un deck dans un contexte donné et retourne un résultat traçable."""

    @property
    @abstractmethod
    def operator_id(self) -> str:
        """Identifiant stable (journalisation, chaînage par l'optimiseur)."""

    @abstractmethod
    def apply(self, context: DeckMutationContext) -> DeckMutationResult:
        """Applique la mutation et retourne avant / après + validations.

        :param context: Paramètres d'exécution.
        :type context: DeckMutationContext
        :returns: Résultat structuré.
        :rtype: DeckMutationResult
        """
