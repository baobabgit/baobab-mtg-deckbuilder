"""Explication textuelle structurée pour une métrique d'évaluation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeckEvaluationExplanation:
    """Détails lisibles pour l'explicabilité (UI, journaux, rapports).

    :param title: Titre court de la métrique ou du diagnostic.
    :type title: str
    :param summary: Synthèse en une ou deux phrases.
    :type summary: str
    :param details: Points additionnels, ordre stable.
    :type details: tuple[str, ...]
    """

    title: str
    summary: str
    details: tuple[str, ...]
