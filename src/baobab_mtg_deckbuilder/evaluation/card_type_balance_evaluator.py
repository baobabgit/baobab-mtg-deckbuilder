"""Évaluateur heuristique : diversité des types de cartes (main)."""

from __future__ import annotations

import math

from baobab_mtg_deckbuilder.deck_statistics.deck_statistics_result import DeckStatisticsResult
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)
from baobab_mtg_deckbuilder.evaluation.deck_metric import DeckMetric


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


class CardTypeBalanceEvaluator:
    """Favorise une répartition non triviale entre catégories de types.

    Entropie de Shannon sur les types du main (hors ``\"?\"``), normalisée par
    ``log(n)`` avec ``n`` le nombre de catégories présentes. Une seule catégorie
    → score modéré ``0,65`` (deck typé mais monolithique).
    """

    METRIC_ID: str = "card_type_diversity"
    DISPLAY_NAME: str = "Équilibre des types de cartes"

    _MONO_TYPE_SCORE: float = 0.65

    # pylint: disable=too-many-locals
    def evaluate(self, stats: DeckStatisticsResult) -> DeckMetric:
        """Calcule la diversité des types sur le main.

        :param stats: Agrégats du deck.
        :type stats: DeckStatisticsResult
        :returns: Métrique avec explication.
        :rtype: DeckMetric
        """
        type_map = {
            label: qty for label, qty in stats.main_type_quantity_by_label.items() if label != "?"
        }
        unknown = stats.main_type_quantity_by_label.get("?", 0)

        if not type_map:
            explanation = DeckEvaluationExplanation(
                title=self.DISPLAY_NAME,
                summary="Aucun type catégorisé (hors « ? ») : score neutre.",
                details=(
                    f"Exemplaires avec type inconnu : {unknown}.",
                    "Enrichir les profils avec type_categories pour activer la métrique.",
                ),
            )
            return DeckMetric(
                metric_id=self.METRIC_ID,
                display_name=self.DISPLAY_NAME,
                raw_score=50.0,
                normalized_score=0.5,
                explanation=explanation,
            )

        quantities = list(type_map.values())
        total = sum(quantities)
        if total <= 0:
            explanation = DeckEvaluationExplanation(
                title=self.DISPLAY_NAME,
                summary="Quantités de types nulles : score neutre.",
                details=(),
            )
            return DeckMetric(
                metric_id=self.METRIC_ID,
                display_name=self.DISPLAY_NAME,
                raw_score=50.0,
                normalized_score=0.5,
                explanation=explanation,
            )

        n_types = len(quantities)
        if n_types == 1:
            normalized = self._MONO_TYPE_SCORE
            summary = (
                f"Une seule catégorie de type ({next(iter(type_map))!r}) : "
                f"score modéré {normalized:.2f}."
            )
        else:
            shares = [q / total for q in quantities]
            entropy = -sum(s * math.log(s) for s in shares if s > 0)
            max_h = math.log(n_types)
            normalized = _clamp01(entropy / max_h) if max_h > 0 else 1.0
            summary = f"Diversité des types ({n_types} catégories) : {normalized:.2f}."

        raw = 100.0 * normalized
        top = sorted(type_map.items(), key=lambda item: (-item[1], item[0].lower()))[:5]
        top_txt = ", ".join(f"{name}:{qty}" for name, qty in top)
        details = [
            f"Répartition (extraits) : {top_txt}.",
            f"Total exemplaires typés : {total}.",
            f"Types « ? » : {unknown}.",
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
