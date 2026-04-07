"""Résultat final d'une optimisation : meilleur état, historique, motif d'arrêt."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.optimization.deck_optimization_iteration import (
    DeckOptimizationIteration,
)
from baobab_mtg_deckbuilder.optimization.deck_optimization_request import DeckOptimizationRequest
from baobab_mtg_deckbuilder.optimization.deck_search_state import DeckSearchState


@dataclass(frozen=True, slots=True)
class DeckOptimizationResult:
    """Sortie structurée du moteur pour consommation par l'appelant ou l'UI.

    :param strategy_key: Identifiant de la stratégie ayant produit ce résultat.
    :type strategy_key: str
    :param request: Requête d'origine.
    :type request: DeckOptimizationRequest
    :param best_state: Meilleur candidat rencontré (score final maximal).
    :type best_state: DeckSearchState
    :param iterations: Historique des itérations (longueur <= ``max_iterations``).
    :type iterations: tuple[DeckOptimizationIteration, ...]
    :param stop_reason: Motif d'arrêt lisible (ex. ``max_iterations``, ``stagnation``).
    :type stop_reason: str
    """

    strategy_key: str
    request: DeckOptimizationRequest
    best_state: DeckSearchState
    iterations: tuple[DeckOptimizationIteration, ...]
    stop_reason: str
