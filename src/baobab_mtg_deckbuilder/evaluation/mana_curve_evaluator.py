"""Évaluateur heuristique : adéquation de la courbe de mana à un gabarit construit."""

from __future__ import annotations

from baobab_mtg_deckbuilder.deck_statistics.deck_statistics import MANA_CURVE_CAP
from baobab_mtg_deckbuilder.deck_statistics.deck_statistics_result import DeckStatisticsResult
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)
from baobab_mtg_deckbuilder.evaluation.deck_metric import DeckMetric
from baobab_mtg_deckbuilder.evaluation.heuristic_inputs import main_nonland_spell_quantity


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


# Gabarit lissé (Construit 60-ish) : parts sur les bacs 0 … MANA_CURVE_CAP (dernier = coûts élevés).
_IDEAL_MANA_SHARES: dict[int, float] = {
    0: 0.06,
    1: 0.14,
    2: 0.26,
    3: 0.24,
    4: 0.14,
    5: 0.08,
    6: 0.05,
    7: 0.03,
}


class ManaCurveEvaluator:
    """Compare la distribution observée des CMC (sorts) à un gabarit de référence.

    Score : ``1 - (1/2) * Σ_k |o_k - i_k|`` où ``o`` et ``i`` sont normalisés sur
    les bacs ``0 … MANA_CURVE_CAP`` (distance L1 sur le simplexe, facteur ``1/2``).

    Sans sort analysé, le score neutre est ``0.5`` (données insuffisantes).
    """

    METRIC_ID: str = "mana_curve_similarity"
    DISPLAY_NAME: str = "Courbe de mana (similarité au gabarit)"

    def evaluate(self, stats: DeckStatisticsResult) -> DeckMetric:
        """Calcule la métrique à partir des statistiques du main.

        :param stats: Agrégats issus de
            :class:`~baobab_mtg_deckbuilder.deck_statistics.deck_statistics.DeckStatistics`.
        :type stats: DeckStatisticsResult
        :returns: Métrique nommée avec explication.
        :rtype: DeckMetric
        """
        spell_qty = main_nonland_spell_quantity(stats)
        if spell_qty <= 0:
            explanation = DeckEvaluationExplanation(
                title=self.DISPLAY_NAME,
                summary="Aucun sort non-terrain avec CMC connu ou inconnu dans les agrégats.",
                details=(
                    "Sans courbe exploitable, le score neutre est appliqué (0,5).",
                    f"Exemplaires avec profil manquant (main) : "
                    f"{stats.main_profile_missing_quantity}.",
                ),
            )
            return DeckMetric(
                metric_id=self.METRIC_ID,
                display_name=self.DISPLAY_NAME,
                raw_score=50.0,
                normalized_score=0.5,
                explanation=explanation,
            )

        curve = stats.main_spell_mana_curve
        observed = {
            bucket: curve.get(bucket, 0) / spell_qty for bucket in range(0, MANA_CURVE_CAP + 1)
        }
        ideal = {
            bucket: _IDEAL_MANA_SHARES.get(bucket, 0.0) for bucket in range(0, MANA_CURVE_CAP + 1)
        }
        l1 = sum(abs(observed[bucket] - ideal[bucket]) for bucket in range(0, MANA_CURVE_CAP + 1))
        normalized = _clamp01(1.0 - 0.5 * l1)
        raw = 100.0 * normalized

        top_buckets = sorted(
            curve.items(),
            key=lambda item: (-item[1], item[0]),
        )[:4]
        detail_curve = ", ".join(f"CMC {k}:{v}" for k, v in top_buckets)
        unknown = stats.main_spell_mana_value_unknown_quantity
        details_list = [
            f"Sorts non-terrain comptés : {spell_qty}.",
            f"Pic de courbe : {detail_curve}.",
            f"CMC inconnu (exemplaires) : {unknown}.",
        ]
        if stats.main_profile_missing_quantity:
            details_list.append(
                f"Profils manquants (main) : {stats.main_profile_missing_quantity} "
                "(non inclus dans la courbe)."
            )

        summary = (
            f"Similarité au gabarit : {normalized:.2f} "
            f"(distance L1 normalisée sur les bacs 0–{MANA_CURVE_CAP})."
        )
        explanation = DeckEvaluationExplanation(
            title=self.DISPLAY_NAME,
            summary=summary,
            details=tuple(details_list),
        )
        return DeckMetric(
            metric_id=self.METRIC_ID,
            display_name=self.DISPLAY_NAME,
            raw_score=raw,
            normalized_score=normalized,
            explanation=explanation,
        )
