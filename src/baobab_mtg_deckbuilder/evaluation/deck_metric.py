"""Valeur nommée d'une métrique heuristique (scores + explication)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)


@dataclass(frozen=True, slots=True)
class DeckMetric:
    """Résultat d'une métrique : identifiant stable, scores et explication.

    Le score normalisé est dans l'intervalle ``[0.0, 1.0]`` (plus haut = plus favorable),
    sauf mention contraire dans la docstring de l'évaluateur.

    :param metric_id: Identifiant machine stable (ex. ``\"mana_curve_similarity\"``).
    :type metric_id: str
    :param display_name: Libellé lisible pour affichage ou pondération.
    :type display_name: str
    :param raw_score: Score brut, même échelle que définie par l'évaluateur.
    :type raw_score: float
    :param normalized_score: Score normalisé ``[0, 1]``.
    :type normalized_score: float
    :param explanation: Texte structuré décrivant le calcul et le contexte.
    :type explanation: DeckEvaluationExplanation
    """

    metric_id: str
    display_name: str
    raw_score: float
    normalized_score: float
    explanation: DeckEvaluationExplanation
