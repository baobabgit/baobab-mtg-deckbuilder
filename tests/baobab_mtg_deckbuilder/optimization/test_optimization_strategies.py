"""Tests des stratégies d'optimisation (arrêts, gain, reproductibilité)."""

from __future__ import annotations

import pytest

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.evaluation.deck_evaluation import DeckEvaluation
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_breakdown import DeckEvaluationBreakdown
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_breakdown_line import (
    DeckEvaluationBreakdownLine,
)
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)
from baobab_mtg_deckbuilder.evaluation.deck_metric import DeckMetric
from baobab_mtg_deckbuilder.evaluation.deck_score import DeckScore
from baobab_mtg_deckbuilder.exceptions.deck_mutation_exception import DeckMutationException
from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.mutation.deck_mutation_operator import DeckMutationOperator
from baobab_mtg_deckbuilder.mutation.deck_mutation_result import DeckMutationResult
from baobab_mtg_deckbuilder.mutation.deck_replacement_suggestion import DeckReplacementSuggestion
from baobab_mtg_deckbuilder.mutation.replace_card_operator import ReplaceCardOperator
from baobab_mtg_deckbuilder.optimization.beam_search_optimization_strategy import (
    BeamSearchOptimizationStrategy,
)
from baobab_mtg_deckbuilder.optimization.deck_optimization_request import DeckOptimizationRequest
from baobab_mtg_deckbuilder.optimization.deck_optimization_strategy import DeckOptimizationStrategy
from baobab_mtg_deckbuilder.optimization.hill_climbing_optimization_strategy import (
    HillClimbingOptimizationStrategy,
)
from baobab_mtg_deckbuilder.optimization.iterative_improvement_strategy import (
    IterativeImprovementStrategy,
)
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)
from tests.baobab_mtg_deckbuilder.mutation.constructed_deck_factory import sixty_spell_deck


def _evaluation_from_score(final: float) -> DeckEvaluation:
    exp = DeckEvaluationExplanation("t", "s", ())
    metric = DeckMetric(
        metric_id="t",
        display_name="T",
        raw_score=final,
        normalized_score=final,
        explanation=exp,
    )
    line = DeckEvaluationBreakdownLine(
        metric_id="t",
        display_name="T",
        weight=1.0,
        normalized_score=final,
        weighted_product=final,
        share_of_weighted_sum=1.0,
    )
    bd = DeckEvaluationBreakdown(
        lines=(line,),
        total_weight=1.0,
        weighted_sum=final,
        weighted_average=final,
    )
    sc = DeckScore(
        weighted_average=final,
        global_bonus=0.0,
        global_penalty=0.0,
        final_score=final,
        total_weight=1.0,
    )
    return DeckEvaluation(metrics=(metric,), score=sc, breakdown=bd, explanation=exp)


def _score_extra_spell(deck: Deck) -> DeckEvaluation:
    qty = float(deck.summary().main_quantity_by_english_name.get("ExtraSpell", 0))
    return _evaluation_from_score(min(1.0, qty / 4.0))


class _FailingMutationOperator(DeckMutationOperator):
    """Ne produit jamais de voisin valide."""

    @property
    def operator_id(self) -> str:
        return "failing"

    def apply(self, context: DeckMutationContext) -> DeckMutationResult:
        raise DeckMutationException("mutation impossible de test")


def _replace_extraspell_request(
    *,
    random_seed: int = 0,
    max_iterations: int = 10,
    stagnation_patience: int | None = 2,
) -> DeckOptimizationRequest:
    fmt = ConstructedFormatDefinition()
    deck, pool = sixty_spell_deck(extra_pool_names=("ExtraSpell",))
    suggestion = DeckReplacementSuggestion(
        remove_english_name="Spell 00",
        add_english_name="ExtraSpell",
        section_identifier="main",
        copies=1,
        rationale="Test optimisation.",
    )
    op = ReplaceCardOperator(suggestion)
    return DeckOptimizationRequest(
        format_definition=fmt,
        pool=pool,
        initial_decks=(deck,),
        mutation_operators=(op,),
        random_seed=random_seed,
        max_iterations=max_iterations,
        stagnation_patience=stagnation_patience,
        evaluate_deck=_score_extra_spell,
        beam_width=2,
    )


@pytest.mark.parametrize(
    "strategy",
    [
        HillClimbingOptimizationStrategy(),
        IterativeImprovementStrategy(),
        BeamSearchOptimizationStrategy(),
    ],
)
def test_optimization_from_initial_deck(strategy: DeckOptimizationStrategy) -> None:
    """Départ d'un deck valide : résultat valide et historique non vide."""
    req = _replace_extraspell_request(max_iterations=1, stagnation_patience=None)
    result = strategy.optimize(req)
    assert result.request is req
    assert result.best_state.deck is not None
    report = req.format_definition.validate(result.best_state.deck)
    assert report.is_valid
    assert len(result.iterations) >= 1
    assert result.iterations[-1].best_score >= 0.0


@pytest.mark.parametrize(
    "strategy",
    [
        HillClimbingOptimizationStrategy(),
        IterativeImprovementStrategy(),
        BeamSearchOptimizationStrategy(),
    ],
)
def test_stop_max_iterations(strategy: DeckOptimizationStrategy) -> None:
    """Arrêt sur budget d'itérations."""
    req = _replace_extraspell_request(max_iterations=4, stagnation_patience=None)
    result = strategy.optimize(req)
    assert result.stop_reason == "max_iterations"
    assert len(result.iterations) == 4


def test_stop_stagnation_hill_climbing() -> None:
    """Stagnation lorsqu'aucun voisin n'est produit."""
    fmt = ConstructedFormatDefinition()
    deck, pool = sixty_spell_deck()
    req = DeckOptimizationRequest(
        format_definition=fmt,
        pool=pool,
        initial_decks=(deck,),
        mutation_operators=(_FailingMutationOperator(),),
        evaluate_deck=lambda _d: _evaluation_from_score(0.5),
        max_iterations=100,
        stagnation_patience=2,
    )
    result = HillClimbingOptimizationStrategy().optimize(req)
    assert result.stop_reason == "stagnation"
    assert len(result.iterations) <= 2


def test_simple_score_improvement_hill_climbing() -> None:
    """Un remplacement légal augmente le score objectif."""
    req = _replace_extraspell_request(max_iterations=5, stagnation_patience=None)
    initial_score = _score_extra_spell(req.initial_decks[0]).score.final_score
    result = HillClimbingOptimizationStrategy().optimize(req)
    assert result.best_state.score_value > initial_score + req.score_epsilon
    names = result.best_state.deck.summary().main_quantity_by_english_name
    assert names.get("ExtraSpell", 0) >= 1


def test_reproducibility_with_seed() -> None:
    """Même graine : même deck optimal pour une stratégie déterministe."""
    req_a = _replace_extraspell_request(
        random_seed=12345, max_iterations=3, stagnation_patience=None
    )
    req_b = _replace_extraspell_request(
        random_seed=12345, max_iterations=3, stagnation_patience=None
    )
    strat = HillClimbingOptimizationStrategy()
    ra = strat.optimize(req_a)
    rb = strat.optimize(req_b)
    assert ra.best_state.deck.list_view() == rb.best_state.deck.list_view()
    assert ra.iterations[-1].best_score == rb.iterations[-1].best_score
