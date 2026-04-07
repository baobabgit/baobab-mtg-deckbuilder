"""Stratégie abstraite d'optimisation itérative."""

from __future__ import annotations

from abc import ABC, abstractmethod

from baobab_mtg_deckbuilder.optimization.deck_optimization_request import DeckOptimizationRequest
from baobab_mtg_deckbuilder.optimization.deck_optimization_result import DeckOptimizationResult


class DeckOptimizationStrategy(ABC):
    """Contrat des stratégies : requête typée → résultat avec historique."""

    @property
    @abstractmethod
    def strategy_key(self) -> str:
        """Clé stable (logs, sérialisation, comparaison)."""

    @abstractmethod
    def optimize(self, request: DeckOptimizationRequest) -> DeckOptimizationResult:
        """Exécute la recherche jusqu'aux critères d'arrêt de la requête.

        :param request: Paramètres et budget d'exploration.
        :type request: DeckOptimizationRequest
        :returns: Meilleur état trouvé et journal d'itérations.
        :rtype: DeckOptimizationResult
        """
