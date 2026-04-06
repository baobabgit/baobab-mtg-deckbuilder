"""Évaluation complète : métriques brutes, score, breakdown et explication."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.evaluation.deck_evaluation_breakdown import DeckEvaluationBreakdown
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)
from baobab_mtg_deckbuilder.evaluation.deck_metric import DeckMetric
from baobab_mtg_deckbuilder.evaluation.deck_score import DeckScore


@dataclass(frozen=True, slots=True)
class DeckEvaluation:
    """Vue d'ensemble pour classement, recommandation ou rapport.

    :param metrics: Métriques sources dans l'ordre fourni à l'agrégateur.
    :type metrics: tuple[DeckMetric, ...]
    :param score: Score final et paramètres d'ajustement.
    :type score: DeckScore
    :param breakdown: Répartition détaillée des contributions pondérées.
    :type breakdown: DeckEvaluationBreakdown
    :param explanation: Synthèse lisible de la composition du score.
    :type explanation: DeckEvaluationExplanation
    """

    metrics: tuple[DeckMetric, ...]
    score: DeckScore
    breakdown: DeckEvaluationBreakdown
    explanation: DeckEvaluationExplanation
