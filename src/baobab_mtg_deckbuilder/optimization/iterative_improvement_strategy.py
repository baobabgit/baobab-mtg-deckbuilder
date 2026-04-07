"""Amélioration itérative : meilleur voisin strictement meilleur que l'état courant."""

from __future__ import annotations

from baobab_mtg_deckbuilder.optimization.deck_optimization_request import DeckOptimizationRequest
from baobab_mtg_deckbuilder.optimization.deck_optimization_result import DeckOptimizationResult
from baobab_mtg_deckbuilder.optimization.deck_optimization_strategy import DeckOptimizationStrategy
from baobab_mtg_deckbuilder.optimization.deck_search_state import DeckSearchState
from baobab_mtg_deckbuilder.optimization.optimization_run_support import (
    append_iteration_record,
    build_optimization_result,
    expand_all_neighbors,
    pick_best,
    prepare_single_start_optimization,
    update_stagnation_counter,
)


def _advance_if_best_neighbor(
    current: DeckSearchState,
    global_best: DeckSearchState,
    neighbors: list[DeckSearchState],
    epsilon: float,
) -> tuple[DeckSearchState, DeckSearchState]:
    """Met à jour l'état courant et le meilleur global si un voisin est strictement meilleur."""
    if not neighbors:
        return current, global_best
    best_neighbor = pick_best(neighbors)
    if best_neighbor.score_value <= current.score_value + epsilon:
        return current, global_best
    new_current = best_neighbor
    if new_current.score_value > global_best.score_value + epsilon:
        return new_current, new_current
    return new_current, global_best


class IterativeImprovementStrategy(DeckOptimizationStrategy):
    """À chaque pas, exploration complète du voisinage puis choix du meilleur gain local."""

    @property
    def strategy_key(self) -> str:
        return "iterative_improvement"

    def optimize(self, request: DeckOptimizationRequest) -> DeckOptimizationResult:
        evaluate_deck, current, global_best, iterations = prepare_single_start_optimization(request)
        stagnation_counter = 0
        stop_reason = "max_iterations"

        for it in range(request.max_iterations):
            best_before = global_best.score_value
            neighbors, evaluated_this = expand_all_neighbors(
                current,
                request,
                evaluate_deck,
                it,
            )
            current, global_best = _advance_if_best_neighbor(
                current,
                global_best,
                neighbors,
                request.score_epsilon,
            )

            append_iteration_record(iterations, it, global_best, evaluated_this)
            improved = global_best.score_value > best_before + request.score_epsilon
            stagnation_counter, stop_stag = update_stagnation_counter(
                stagnation_counter, request, improved
            )
            if stop_stag:
                stop_reason = "stagnation"
                break

        return build_optimization_result(
            self.strategy_key, request, global_best, iterations, stop_reason
        )
