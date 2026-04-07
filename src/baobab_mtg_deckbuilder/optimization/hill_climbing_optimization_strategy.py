"""Montée de colline : premier voisin améliorant dans l'ordre des opérateurs."""

from __future__ import annotations

from baobab_mtg_deckbuilder.optimization.deck_optimization_request import DeckOptimizationRequest
from baobab_mtg_deckbuilder.optimization.deck_optimization_result import DeckOptimizationResult
from baobab_mtg_deckbuilder.optimization.deck_optimization_strategy import DeckOptimizationStrategy
from baobab_mtg_deckbuilder.optimization.optimization_run_support import (
    append_iteration_record,
    build_optimization_result,
    first_improving_neighbor,
    prepare_single_start_optimization,
    update_stagnation_counter,
)


class HillClimbingOptimizationStrategy(DeckOptimizationStrategy):
    """Recherche locale : à chaque itération, premier successeur strictement meilleur."""

    @property
    def strategy_key(self) -> str:
        return "hill_climbing"

    def optimize(self, request: DeckOptimizationRequest) -> DeckOptimizationResult:
        evaluate_deck, current, global_best, iterations = prepare_single_start_optimization(request)
        stagnation_counter = 0
        stop_reason = "max_iterations"
        eps = request.score_epsilon

        for it in range(request.max_iterations):
            best_before = global_best.score_value
            chosen, evaluated_this = first_improving_neighbor(
                current,
                request,
                evaluate_deck,
                it,
            )
            if chosen is not None:
                current = chosen
                if current.score_value > global_best.score_value + eps:
                    global_best = current

            append_iteration_record(iterations, it, global_best, evaluated_this)
            improved = global_best.score_value > best_before + eps
            stagnation_counter, stop_stag = update_stagnation_counter(
                stagnation_counter, request, improved
            )
            if stop_stag:
                stop_reason = "stagnation"
                break

        return build_optimization_result(
            self.strategy_key, request, global_best, iterations, stop_reason
        )
