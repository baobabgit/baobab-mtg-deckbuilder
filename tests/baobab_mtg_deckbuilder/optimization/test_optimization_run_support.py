"""Tests des utilitaires d'exécution d'optimisation."""

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
from baobab_mtg_deckbuilder.exceptions.deck_optimization_exception import DeckOptimizationException
from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.mutation.deck_mutation_operator import DeckMutationOperator
from baobab_mtg_deckbuilder.mutation.deck_mutation_result import DeckMutationResult
from baobab_mtg_deckbuilder.optimization.deck_optimization_request import DeckOptimizationRequest
from baobab_mtg_deckbuilder.optimization.optimization_run_support import resolve_evaluate_deck
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)
from tests.baobab_mtg_deckbuilder.mutation.constructed_deck_factory import sixty_spell_deck


def _zero_eval(_deck: Deck) -> DeckEvaluation:
    exp = DeckEvaluationExplanation("t", "s", ())
    metric = DeckMetric(
        metric_id="t",
        display_name="T",
        raw_score=0.0,
        normalized_score=0.0,
        explanation=exp,
    )
    line = DeckEvaluationBreakdownLine(
        metric_id="t",
        display_name="T",
        weight=1.0,
        normalized_score=0.0,
        weighted_product=0.0,
        share_of_weighted_sum=1.0,
    )
    bd = DeckEvaluationBreakdown(
        lines=(line,),
        total_weight=1.0,
        weighted_sum=0.0,
        weighted_average=0.0,
    )
    sc = DeckScore(
        weighted_average=0.0,
        global_bonus=0.0,
        global_penalty=0.0,
        final_score=0.0,
        total_weight=1.0,
    )
    return DeckEvaluation(metrics=(metric,), score=sc, breakdown=bd, explanation=exp)


class _DummyOperator(DeckMutationOperator):
    @property
    def operator_id(self) -> str:
        return "dummy"

    def apply(self, context: DeckMutationContext) -> DeckMutationResult:
        raise NotImplementedError


class TestResolveEvaluateDeck:
    """Résolution de la fonction de score."""

    def test_uses_custom_evaluate_deck_when_set(self) -> None:
        """Priorité à ``evaluate_deck``."""
        fmt = ConstructedFormatDefinition()
        deck, pool = sixty_spell_deck()
        req = DeckOptimizationRequest(
            format_definition=fmt,
            pool=pool,
            initial_decks=(deck,),
            mutation_operators=(_DummyOperator(),),
            evaluate_deck=_zero_eval,
            analytic_provider=None,
        )
        fn = resolve_evaluate_deck(req)
        assert fn(deck).score.final_score == 0.0

    def test_raises_when_no_provider_and_no_evaluate(self) -> None:
        """Branche défensive si la requête est incohérente."""
        fmt = ConstructedFormatDefinition()
        deck, pool = sixty_spell_deck()
        req = DeckOptimizationRequest(
            format_definition=fmt,
            pool=pool,
            initial_decks=(deck,),
            mutation_operators=(_DummyOperator(),),
            evaluate_deck=_zero_eval,
        )
        object.__setattr__(req, "evaluate_deck", None)
        object.__setattr__(req, "analytic_provider", None)
        with pytest.raises(DeckOptimizationException, match="analytic_provider"):
            resolve_evaluate_deck(req)
