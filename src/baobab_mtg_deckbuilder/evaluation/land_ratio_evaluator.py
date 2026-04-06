"""Évaluateur heuristique : ratio de terrains dans le main."""

from __future__ import annotations

from baobab_mtg_deckbuilder.deck_statistics.deck_statistics_result import DeckStatisticsResult
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)
from baobab_mtg_deckbuilder.evaluation.deck_metric import DeckMetric
from baobab_mtg_deckbuilder.evaluation.heuristic_inputs import main_deck_card_quantity


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


class LandRatioEvaluator:
    """Évalue le ratio terrains / cartes du main autour d'une cible Construit.

    Cible par défaut ``38 %`` ; score normalisé triangulaire :
    ``max(0, 1 - |r - cible| / demi-largeur)`` avec demi-largeur ``0,12``.

    Le numérateur utilise :py:attr:`DeckStatisticsResult.main_land_quantity` ;
    le dénominateur est le nombre total de cartes listées dans le main. Les cartes
    sans profil ne sont pas comptées comme terrains dans le numérateur (voir détails).
    """

    METRIC_ID: str = "main_land_ratio"
    DISPLAY_NAME: str = "Ratio de terrains (main)"

    TARGET_RATIO: float = 0.38
    HALF_WIDTH: float = 0.12

    def evaluate(self, stats: DeckStatisticsResult) -> DeckMetric:
        """Calcule la métrique pour le main.

        :param stats: Agrégats du deck.
        :type stats: DeckStatisticsResult
        :returns: Métrique avec explication.
        :rtype: DeckMetric
        """
        main_size = main_deck_card_quantity(stats)
        if main_size <= 0:
            explanation = DeckEvaluationExplanation(
                title=self.DISPLAY_NAME,
                summary="Main vide : score neutre.",
                details=("Aucune carte dans le main selon les agrégats.",),
            )
            return DeckMetric(
                metric_id=self.METRIC_ID,
                display_name=self.DISPLAY_NAME,
                raw_score=50.0,
                normalized_score=0.5,
                explanation=explanation,
            )

        lands = stats.main_land_quantity
        ratio = lands / main_size
        deviation = abs(ratio - self.TARGET_RATIO)
        normalized = _clamp01(1.0 - deviation / self.HALF_WIDTH)
        raw = 100.0 * normalized

        details = [
            f"Terrains reconnus : {lands} sur {main_size} cartes (ratio {ratio:.1%}).",
            f"Cible heuristique : {self.TARGET_RATIO:.0%} (±{self.HALF_WIDTH:.0%}).",
        ]
        if stats.main_profile_missing_quantity:
            details.append(
                f"Profils manquants : {stats.main_profile_missing_quantity} "
                "(peuvent sous-estimer les terrains si non typés)."
            )

        summary = (
            f"Écart à la cible {self.TARGET_RATIO:.0%} : {deviation:.1%} "
            f"→ score normalisé {normalized:.2f}."
        )
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
