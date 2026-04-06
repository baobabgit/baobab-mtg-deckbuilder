"""Évaluateur heuristique : équilibre des couleurs WUBRG (pips du main)."""

from __future__ import annotations

import math

from baobab_mtg_deckbuilder.deck_statistics.deck_statistics_result import DeckStatisticsResult
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)
from baobab_mtg_deckbuilder.evaluation.deck_metric import DeckMetric

_WUBRG: tuple[str, ...] = ("W", "U", "B", "R", "G")


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


class ColorBalanceEvaluator:
    """Mesure l'équilibre des contributions WUBRG via entropie normalisée.

    Seules les couleurs avec pip strictement positif sont prises en compte.
    Mono-couleur : score maximal (1,0). Multi : entropie de Shannon / ``log(n)``.

    Les libellés ``\"C\"`` et ``\"?\"`` sont exclus de ce calcul (voir métrique
    « cohérence de base » pour les incertitudes).
    """

    METRIC_ID: str = "wubrg_color_balance"
    DISPLAY_NAME: str = "Équilibre des couleurs (WUBRG)"

    def evaluate(self, stats: DeckStatisticsResult) -> DeckMetric:
        """Calcule la métrique sur les pips du main.

        :param stats: Agrégats du deck.
        :type stats: DeckStatisticsResult
        :returns: Métrique avec explication.
        :rtype: DeckMetric
        """
        counts = [stats.main_color_quantity_by_label.get(c, 0) for c in _WUBRG]
        active = [c for c in counts if c > 0]
        total = sum(active)
        unknown = stats.main_color_quantity_by_label.get("?", 0)
        colorless = stats.main_color_quantity_by_label.get("C", 0)

        if total <= 0:
            explanation = DeckEvaluationExplanation(
                title=self.DISPLAY_NAME,
                summary="Aucun pip WUBRG enregistré : score neutre.",
                details=(
                    f"Pips « ? » : {unknown}, « C » : {colorless}.",
                    "Fournir des identités de couleur sur le main pour activer la métrique.",
                ),
            )
            return DeckMetric(
                metric_id=self.METRIC_ID,
                display_name=self.DISPLAY_NAME,
                raw_score=50.0,
                normalized_score=0.5,
                explanation=explanation,
            )

        if len(active) == 1:
            normalized = 1.0
            summary = "Mono-couleur WUBRG : équilibre maximal (un seul pôle actif)."
        else:
            shares = [c / total for c in active]
            entropy = -sum(s * math.log(s) for s in shares if s > 0)
            max_h = math.log(len(active))
            normalized = _clamp01(entropy / max_h) if max_h > 0 else 1.0
            summary = (
                f"Entropie normalisée sur {len(active)} couleurs actives : " f"{normalized:.2f}."
            )

        raw = 100.0 * normalized
        details = [
            f"Pips WUBRG total (hors C/?) : {total}.",
            f"Couleurs actives : {len(active)}.",
            f"Pips « ? » : {unknown}, « C » : {colorless}.",
        ]
        explanation = DeckEvaluationExplanation(
            title=self.DISPLAY_NAME,
            summary=summary,
            details=tuple(details),
        )
        return DeckMetric(
            metric_id=self.METRIC_ID,
            display_name=self.DISPLAY_NAME,
            raw_score=raw,
            normalized_score=normalized,
            explanation=explanation,
        )
