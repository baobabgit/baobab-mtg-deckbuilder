"""Tests pour :class:`DeckOptimizationRequest`."""

import pytest

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
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
from baobab_mtg_deckbuilder.optimization.hill_climbing_optimization_strategy import (
    HillClimbingOptimizationStrategy,
)
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)
from tests.baobab_mtg_deckbuilder.mutation.constructed_deck_factory import sixty_spell_deck


def _noop_eval(_deck: Deck) -> DeckEvaluation:
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
    """Opérateur minimal (jamais invoqué par ces tests de requête)."""

    @property
    def operator_id(self) -> str:
        return "dummy"

    def apply(self, context: DeckMutationContext) -> DeckMutationResult:
        raise NotImplementedError


class TestDeckOptimizationRequest:
    """Validation de configuration."""

    def test_requires_initial_deck(self) -> None:
        """Au moins un deck initial."""
        fmt = ConstructedFormatDefinition()
        _, pool = sixty_spell_deck()
        with pytest.raises(DeckOptimizationException, match="Au moins un deck initial"):
            DeckOptimizationRequest(
                format_definition=fmt,
                pool=pool,
                initial_decks=(),
                mutation_operators=(_DummyOperator(),),
                evaluate_deck=_noop_eval,
            )

    def test_requires_scoring_source(self) -> None:
        """Évaluateur ou fournisseur analytique."""
        fmt = ConstructedFormatDefinition()
        deck, pool = sixty_spell_deck()
        with pytest.raises(DeckOptimizationException, match="noter les decks"):
            DeckOptimizationRequest(
                format_definition=fmt,
                pool=pool,
                initial_decks=(deck,),
                mutation_operators=(_DummyOperator(),),
                evaluate_deck=None,
                analytic_provider=None,
            )

    def test_accepts_evaluate_deck_without_provider(self) -> None:
        """``evaluate_deck`` seul suffit."""
        fmt = ConstructedFormatDefinition()
        deck, pool = sixty_spell_deck()
        req = DeckOptimizationRequest(
            format_definition=fmt,
            pool=pool,
            initial_decks=(deck,),
            mutation_operators=(_DummyOperator(),),
            evaluate_deck=_noop_eval,
            analytic_provider=None,
        )
        assert req.evaluate_deck is not None

    def test_requires_positive_max_iterations(self) -> None:
        """``max_iterations`` >= 1."""
        fmt = ConstructedFormatDefinition()
        deck, pool = sixty_spell_deck()
        with pytest.raises(DeckOptimizationException, match="max_iterations"):
            DeckOptimizationRequest(
                format_definition=fmt,
                pool=pool,
                initial_decks=(deck,),
                mutation_operators=(_DummyOperator(),),
                evaluate_deck=_noop_eval,
                max_iterations=0,
            )

    def test_requires_positive_beam_width(self) -> None:
        """``beam_width`` >= 1."""
        fmt = ConstructedFormatDefinition()
        deck, pool = sixty_spell_deck()
        with pytest.raises(DeckOptimizationException, match="beam_width"):
            DeckOptimizationRequest(
                format_definition=fmt,
                pool=pool,
                initial_decks=(deck,),
                mutation_operators=(_DummyOperator(),),
                evaluate_deck=_noop_eval,
                beam_width=0,
            )

    def test_invalid_initial_deck_rejected_by_strategy(self) -> None:
        """Deck initial illégal : exception avant la boucle."""
        fmt = ConstructedFormatDefinition()
        main_bad = tuple(DeckCardEntry(f"Spell {i:02d}", 4) for i in range(14))
        bad_deck = Deck.from_sections(DeckSection.main(main_bad), DeckSection.sideboard(()))
        entries = [CardPoolEntry(f"Spell {i:02d}", 4) for i in range(15)]
        pool = CardPool.from_entries(tuple(entries), pool_kind="physical")
        req = DeckOptimizationRequest(
            format_definition=fmt,
            pool=pool,
            initial_decks=(bad_deck,),
            mutation_operators=(_DummyOperator(),),
            evaluate_deck=_noop_eval,
            stagnation_patience=None,
        )
        with pytest.raises(DeckOptimizationException, match="invalide"):
            HillClimbingOptimizationStrategy().optimize(req)
