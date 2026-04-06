"""Score agrégé final et paramètres d'ajustement."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeckScore:
    """Résultat numérique explicite (jamais opaque : voir :class:`DeckEvaluationBreakdown`).

    :param weighted_average: Moyenne pondérée des scores normalisés, avant ajustement.
    :type weighted_average: float
    :param global_bonus: Bonus additif sur l'échelle ``[0, 1]`` (après moyenne).
    :type global_bonus: float
    :param global_penalty: Pénalité additive (soustraite après la moyenne).
    :type global_penalty: float
    :param final_score: ``clamp(weighted_average + bonus - pénalité, 0, 1)``.
    :type final_score: float
    :param total_weight: Somme des poids ayant servi à la moyenne.
    :type total_weight: float
    """

    weighted_average: float
    global_bonus: float
    global_penalty: float
    final_score: float
    total_weight: float
