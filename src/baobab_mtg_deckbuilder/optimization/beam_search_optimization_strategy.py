"""Recherche en faisceau : élargissement parallèle puis sélection des ``beam_width`` meilleurs."""

from __future__ import annotations

from collections.abc import Callable

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.evaluation.deck_evaluation import DeckEvaluation
from baobab_mtg_deckbuilder.optimization.deck_optimization_iteration import (
    DeckOptimizationIteration,
)
from baobab_mtg_deckbuilder.optimization.deck_optimization_request import DeckOptimizationRequest
from baobab_mtg_deckbuilder.optimization.deck_optimization_result import DeckOptimizationResult
from baobab_mtg_deckbuilder.optimization.deck_optimization_strategy import DeckOptimizationStrategy
from baobab_mtg_deckbuilder.optimization.deck_search_state import DeckSearchState
from baobab_mtg_deckbuilder.optimization.optimization_run_support import (
    append_iteration_record,
    assert_initial_decks_valid,
    build_initial_states,
    build_optimization_result,
    dedupe_best_per_deck,
    expand_all_neighbors,
    pick_best,
    resolve_evaluate_deck,
    sort_states_descending,
    update_stagnation_counter,
)


def _beam_expand_once(
    beam: list[DeckSearchState],
    *,
    request: DeckOptimizationRequest,
    evaluate_deck: Callable[[Deck], DeckEvaluation],
    iteration_index: int,
    global_best: DeckSearchState,
    eps: float,
) -> tuple[list[DeckSearchState], DeckSearchState, int]:
    """Élargit chaque état du faisceau, déduplique et tronque à ``beam_width``."""
    merged: list[DeckSearchState] = []
    evaluated = 0
    for slot, state in enumerate(beam):
        neighbors, count = expand_all_neighbors(
            state,
            request,
            evaluate_deck,
            iteration_index,
            beam_slot=slot,
        )
        evaluated += count
        merged.extend(neighbors)
    if not merged:
        return beam, global_best, evaluated
    unique = dedupe_best_per_deck(merged, eps)
    new_beam = sort_states_descending(unique)[: request.beam_width]
    new_global = pick_best([global_best, pick_best(new_beam)])
    return new_beam, new_global, evaluated


class BeamSearchOptimizationStrategy(DeckOptimizationStrategy):
    """Maintient jusqu'à ``beam_width`` candidats ; fusion et troncature déterministes."""

    @property
    def strategy_key(self) -> str:
        return "beam_search"

    def optimize(self, request: DeckOptimizationRequest) -> DeckOptimizationResult:
        assert_initial_decks_valid(request)
        evaluate_deck = resolve_evaluate_deck(request)
        initial_states = build_initial_states(request, evaluate_deck)
        beam = sort_states_descending(initial_states)[: request.beam_width]
        global_best = pick_best(beam)
        iterations: list[DeckOptimizationIteration] = []
        stagnation_counter = 0
        stop_reason = "max_iterations"
        eps = request.score_epsilon

        for it in range(request.max_iterations):
            best_before = global_best.score_value
            beam, global_best, evaluated_this = _beam_expand_once(
                beam,
                request=request,
                evaluate_deck=evaluate_deck,
                iteration_index=it,
                global_best=global_best,
                eps=eps,
            )
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
