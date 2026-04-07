"""Journal d'une itération de recherche."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeckOptimizationIteration:
    """Une ligne d'historique pour l'explicabilité et le débogage.

    :param iteration_index: Indice de l'itération (0-based).
    :type iteration_index: int
    :param best_score: Meilleur score observé depuis le début jusqu'à cette itération.
    :type best_score: float
    :param evaluated_mutations: Nombre de mutations tentées avec succès (deck valide).
    :type evaluated_mutations: int
    """

    iteration_index: int
    best_score: float
    evaluated_mutations: int
