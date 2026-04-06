"""Une ligne du breakdown d'évaluation pondérée."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeckEvaluationBreakdownLine:
    """Contribution d'une métrique au score agrégé.

    :param metric_id: Identifiant stable de la métrique.
    :type metric_id: str
    :param display_name: Libellé lisible.
    :type display_name: str
    :param weight: Poids strictement positif utilisé dans l'agrégat.
    :type weight: float
    :param normalized_score: Score normalisé ``[0, 1]`` de la métrique.
    :type normalized_score: float
    :param weighted_product: Produit ``poids × score_normalisé``.
    :type weighted_product: float
    :param share_of_weighted_sum: Part ``weighted_product / Σ(w×s)`` si le dénominateur
        est positif, sinon ``0.0``.
    :type share_of_weighted_sum: float
    """

    metric_id: str
    display_name: str
    weight: float
    normalized_score: float
    weighted_product: float
    share_of_weighted_sum: float
