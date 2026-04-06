"""Breakdown déterministe du calcul de score pondéré."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.evaluation.deck_evaluation_breakdown_line import (
    DeckEvaluationBreakdownLine,
)


@dataclass(frozen=True, slots=True)
class DeckEvaluationBreakdown:
    """Détail des contributions avant bonus / pénalité globaux.

    Les lignes sont triées par ``metric_id`` (insensible à la casse puis lexicographique).

    :param lines: Une entrée par métrique pondérée.
    :type lines: tuple[DeckEvaluationBreakdownLine, ...]
    :param total_weight: Somme des poids des lignes.
    :type total_weight: float
    :param weighted_sum: Somme des ``poids × score_normalisé``.
    :type weighted_sum: float
    :param weighted_average: ``weighted_sum / total_weight`` si ``total_weight > 0``,
        sinon ``0.0``.
    :type weighted_average: float
    """

    lines: tuple[DeckEvaluationBreakdownLine, ...]
    total_weight: float
    weighted_sum: float
    weighted_average: float
