"""Utilitaires partagés par les stratégies (évaluation, voisinage, tri)."""

from __future__ import annotations

from collections.abc import Callable

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.evaluation.deck_evaluation import DeckEvaluation
from baobab_mtg_deckbuilder.exceptions.deck_mutation_exception import DeckMutationException
from baobab_mtg_deckbuilder.exceptions.deck_optimization_exception import DeckOptimizationException
from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.optimization.deck_optimization_iteration import (
    DeckOptimizationIteration,
)
from baobab_mtg_deckbuilder.optimization.deck_optimization_request import DeckOptimizationRequest
from baobab_mtg_deckbuilder.optimization.deck_optimization_result import DeckOptimizationResult
from baobab_mtg_deckbuilder.optimization.deck_search_state import DeckSearchState
from baobab_mtg_deckbuilder.optimization.optimization_evaluation import (
    default_optimization_evaluation,
)


def resolve_evaluate_deck(request: DeckOptimizationRequest) -> Callable[[Deck], DeckEvaluation]:
    """Construit la fonction de notation à partir de la requête."""
    if request.evaluate_deck is not None:
        return request.evaluate_deck
    provider = request.analytic_provider
    if provider is None:
        raise DeckOptimizationException(
            "analytic_provider requis lorsque evaluate_deck est absent."
        )

    def _wrapped(deck: Deck) -> DeckEvaluation:
        return default_optimization_evaluation(deck, provider)

    return _wrapped


def assert_initial_decks_valid(request: DeckOptimizationRequest) -> None:
    """Vérifie que chaque deck initial satisfait le format."""
    for deck in request.initial_decks:
        report = request.format_definition.validate(deck)
        if not report.is_valid:
            raise DeckOptimizationException(
                "Un deck initial est invalide pour le format demandé "
                f"({report.error_count} erreur(s) de validation)."
            )


def deck_sort_key(
    deck: Deck,
) -> tuple[int, tuple[tuple[str, int], ...], tuple[tuple[str, int], ...]]:
    """Clé déterministe pour départager les scores ex aequo."""
    lv = deck.list_view()
    main_k = tuple((e.english_name, e.quantity) for e in lv.main_entries)
    side_k = tuple((e.english_name, e.quantity) for e in lv.sideboard_entries)
    return (deck.summary().total_quantity, main_k, side_k)


def sort_states_descending(states: list[DeckSearchState]) -> list[DeckSearchState]:
    """Trie par score décroissant puis par empreinte de deck."""
    return sorted(
        states,
        key=lambda s: (-s.score_value, deck_sort_key(s.deck)),
    )


def pick_best(states: list[DeckSearchState]) -> DeckSearchState:
    """Retourne l'état de score maximal (tie-break déterministe)."""
    if not states:
        raise DeckOptimizationException("Liste d'états vide pour pick_best.")
    return sort_states_descending(states)[0]


def build_initial_states(
    request: DeckOptimizationRequest,
    evaluate_deck: Callable[[Deck], DeckEvaluation],
) -> list[DeckSearchState]:
    """Évalue tous les decks initiaux."""
    return [DeckSearchState(d, evaluate_deck(d)) for d in request.initial_decks]


def make_mutation_context(
    deck: Deck,
    request: DeckOptimizationRequest,
    iteration_index: int,
    operator_index: int,
    *,
    beam_slot: int = 0,
) -> DeckMutationContext:
    """Construit un contexte de mutation avec graine déterministe."""
    return DeckMutationContext(
        deck=deck,
        format_definition=request.format_definition,
        pool=request.pool,
        random_seed=request.random_seed
        + iteration_index * 1_000_003
        + beam_slot * 17_893
        + operator_index * 97_531,
        analytic_provider=request.analytic_provider,
    )


def try_evaluated_successor(
    request: DeckOptimizationRequest,
    iteration_index: int,
    operator_index: int,
    evaluate_deck: Callable[[Deck], DeckEvaluation],
    deck: Deck,
    *,
    beam_slot: int = 0,
) -> tuple[DeckSearchState | None, bool]:
    """Applique l'opérateur à l'index donné ; retourne (état, True) si évalué avec succès."""
    operator = request.mutation_operators[operator_index]
    ctx = make_mutation_context(
        deck,
        request,
        iteration_index,
        operator_index,
        beam_slot=beam_slot,
    )
    try:
        mut_res = operator.apply(ctx)
    except DeckMutationException:
        return None, False
    if not mut_res.validation_report_after.is_valid:
        return None, False
    state = DeckSearchState(mut_res.deck_after, evaluate_deck(mut_res.deck_after))
    return state, True


def first_improving_neighbor(
    current: DeckSearchState,
    request: DeckOptimizationRequest,
    evaluate_deck: Callable[[Deck], DeckEvaluation],
    iteration_index: int,
    *,
    beam_slot: int = 0,
) -> tuple[DeckSearchState | None, int]:
    """Premier voisin strictement meilleur (ordre opérateurs) et nombre d'évaluations réussies."""
    eps = request.score_epsilon
    evaluated = 0
    for op_index in range(len(request.mutation_operators)):
        succ, ok = try_evaluated_successor(
            request,
            iteration_index,
            op_index,
            evaluate_deck,
            current.deck,
            beam_slot=beam_slot,
        )
        if not ok:
            continue
        evaluated += 1
        if succ is not None and succ.score_value > current.score_value + eps:
            return succ, evaluated
    return None, evaluated


def expand_all_neighbors(
    current: DeckSearchState,
    request: DeckOptimizationRequest,
    evaluate_deck: Callable[[Deck], DeckEvaluation],
    iteration_index: int,
    *,
    beam_slot: int = 0,
) -> tuple[list[DeckSearchState], int]:
    """Tous les voisins valides évalués pour un parent."""
    neighbors: list[DeckSearchState] = []
    evaluated = 0
    for op_index in range(len(request.mutation_operators)):
        succ, ok = try_evaluated_successor(
            request,
            iteration_index,
            op_index,
            evaluate_deck,
            current.deck,
            beam_slot=beam_slot,
        )
        if ok and succ is not None:
            evaluated += 1
            neighbors.append(succ)
    return neighbors, evaluated


def dedupe_best_per_deck(
    states: list[DeckSearchState],
    epsilon: float,
) -> list[DeckSearchState]:
    """Conserve le meilleur score par empreinte de deck."""
    by_key: dict[
        tuple[int, tuple[tuple[str, int], ...], tuple[tuple[str, int], ...]],
        DeckSearchState,
    ] = {}
    for state in states:
        key = deck_sort_key(state.deck)
        previous = by_key.get(key)
        if previous is None or state.score_value > previous.score_value + epsilon:
            by_key[key] = state
    return list(by_key.values())


def append_iteration_record(
    iterations: list[DeckOptimizationIteration],
    iteration_index: int,
    global_best: DeckSearchState,
    evaluated_mutations: int,
) -> None:
    """Ajoute une entrée à l'historique d'optimisation."""
    iterations.append(
        DeckOptimizationIteration(
            iteration_index=iteration_index,
            best_score=global_best.score_value,
            evaluated_mutations=evaluated_mutations,
        )
    )


def update_stagnation_counter(
    stagnation_counter: int,
    request: DeckOptimizationRequest,
    global_best_improved: bool,
) -> tuple[int, bool]:
    """Met à jour la stagnation ; le booléen indique un arrêt sur patience atteinte."""
    if global_best_improved:
        return 0, False
    next_count = stagnation_counter + 1
    patience = request.stagnation_patience
    if patience is None:
        return next_count, False
    return next_count, next_count >= patience


def build_optimization_result(
    strategy_key: str,
    request: DeckOptimizationRequest,
    global_best: DeckSearchState,
    iterations: list[DeckOptimizationIteration],
    stop_reason: str,
) -> DeckOptimizationResult:
    """Assemble le résultat final."""
    return DeckOptimizationResult(
        strategy_key=strategy_key,
        request=request,
        best_state=global_best,
        iterations=tuple(iterations),
        stop_reason=stop_reason,
    )


def prepare_single_start_optimization(
    request: DeckOptimizationRequest,
) -> tuple[
    Callable[[Deck], DeckEvaluation],
    DeckSearchState,
    DeckSearchState,
    list[DeckOptimizationIteration],
]:
    """Valide les entrées, évalue les decks initiaux et retourne l'état de départ unique."""
    assert_initial_decks_valid(request)
    evaluate_deck = resolve_evaluate_deck(request)
    initial_states = build_initial_states(request, evaluate_deck)
    start = pick_best(initial_states)
    return evaluate_deck, start, start, []
