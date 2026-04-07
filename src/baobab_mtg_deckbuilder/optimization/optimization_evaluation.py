"""Évaluation standard pour l'optimisation (statistiques + agrégation pondérée)."""

from __future__ import annotations

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck_statistics.card_analytic_provider_protocol import (
    CardAnalyticProviderProtocol,
)
from baobab_mtg_deckbuilder.deck_statistics.deck_statistics import DeckStatistics
from baobab_mtg_deckbuilder.evaluation.card_type_balance_evaluator import CardTypeBalanceEvaluator
from baobab_mtg_deckbuilder.evaluation.color_balance_evaluator import ColorBalanceEvaluator
from baobab_mtg_deckbuilder.evaluation.deck_evaluation import DeckEvaluation
from baobab_mtg_deckbuilder.evaluation.land_ratio_evaluator import LandRatioEvaluator
from baobab_mtg_deckbuilder.evaluation.mana_base_consistency_evaluator import (
    ManaBaseConsistencyEvaluator,
)
from baobab_mtg_deckbuilder.evaluation.mana_curve_evaluator import ManaCurveEvaluator
from baobab_mtg_deckbuilder.evaluation.weighted_score_aggregator import WeightedScoreAggregator


def default_optimization_evaluation(
    deck: Deck,
    analytic_provider: CardAnalyticProviderProtocol,
) -> DeckEvaluation:
    """Calcule une :class:`~baobab_mtg_deckbuilder.evaluation.deck_evaluation.DeckEvaluation` MVP.

    Même composition que les exemples agrégés du paquet : cinq métriques heuristiques et
    :class:`WeightedScoreAggregator` avec poids par défaut.

    :param deck: Deck à noter.
    :type deck: Deck
    :param analytic_provider: Source de profils pour :meth:`DeckStatistics.analyze`.
    :type analytic_provider: CardAnalyticProviderProtocol
    :returns: Évaluation complète.
    :rtype: DeckEvaluation
    """
    stats = DeckStatistics.analyze(deck, analytic_provider)
    metrics = (
        ManaCurveEvaluator().evaluate(stats),
        LandRatioEvaluator().evaluate(stats),
        ColorBalanceEvaluator().evaluate(stats),
        ManaBaseConsistencyEvaluator().evaluate(stats),
        CardTypeBalanceEvaluator().evaluate(stats),
    )
    return WeightedScoreAggregator().aggregate(metrics)
