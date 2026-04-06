"""Agrégateur pondéré des :class:`DeckMetric` vers un :class:`DeckEvaluation`."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from baobab_mtg_deckbuilder.evaluation.deck_evaluation import DeckEvaluation
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_breakdown import DeckEvaluationBreakdown
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_breakdown_line import (
    DeckEvaluationBreakdownLine,
)
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)
from baobab_mtg_deckbuilder.evaluation.deck_metric import DeckMetric
from baobab_mtg_deckbuilder.evaluation.deck_score import DeckScore
from baobab_mtg_deckbuilder.evaluation.default_metric_weights import default_metric_weights
from baobab_mtg_deckbuilder.exceptions.deck_evaluation_exception import DeckEvaluationException


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _non_negative(name: str, value: float) -> float:
    if value < 0:
        raise DeckEvaluationException(f"{name} doit être positif ou nul (reçu {value!r}).")
    return float(value)


def _validate_and_sort_weights(weights: Mapping[str, float]) -> tuple[tuple[str, float], ...]:
    items: list[tuple[str, float]] = []
    for key, raw in weights.items():
        w = float(raw)
        if w < 0:
            raise DeckEvaluationException(f"Poids négatif pour {key!r} : {w!r}.")
        if w > 0:
            items.append((key, w))
    if not items:
        raise DeckEvaluationException(
            "Au moins un poids strictement positif est requis pour l'agrégation."
        )
    return tuple(sorted(items, key=lambda item: (item[0].lower(), item[0])))


def _metrics_by_id(metrics: Sequence[DeckMetric]) -> dict[str, DeckMetric]:
    by_id: dict[str, DeckMetric] = {}
    for metric in metrics:
        mid = metric.metric_id
        if mid in by_id:
            raise DeckEvaluationException(f"Métrique dupliquée pour l'id {mid!r}.")
        by_id[mid] = metric
    return by_id


def _weighted_rows_and_totals(
    weight_items: tuple[tuple[str, float], ...],
    by_id: dict[str, DeckMetric],
) -> tuple[
    tuple[tuple[str, str, float, float, float], ...],
    float,
    float,
]:
    row_data: list[tuple[str, str, float, float, float]] = []
    weighted_sum = 0.0
    total_weight = 0.0
    for mid, weight in weight_items:
        if mid not in by_id:
            raise DeckEvaluationException(f"Métrique requise absente pour l'agrégation : {mid!r}.")
        m = by_id[mid]
        s = _clamp01(m.normalized_score)
        product = weight * s
        weighted_sum += product
        total_weight += weight
        row_data.append((mid, m.display_name, weight, s, product))
    return tuple(row_data), weighted_sum, total_weight


class WeightedScoreAggregator:
    """Combine des métriques normalisées avec des poids configurables.

    La moyenne pondérée utilise uniquement les métriques listées dans la table
    de poids (identifiants ``metric_id``). Toute entrée à poids strictement positif
    doit avoir une métrique correspondante dans l'appel à :meth:`aggregate`.

    Le score final est ``clamp(moyenne + bonus_global - pénalité_global, 0, 1)``.
    """

    def __init__(
        self,
        weights: Mapping[str, float] | None = None,
        *,
        global_bonus: float = 0.0,
        global_penalty: float = 0.0,
    ) -> None:
        """Construit l'agrégateur.

        :param weights: Table ``metric_id → poids`` ; ``None`` équivaut à
            ``default_metric_weights()`` (voir ce module).
        :type weights: collections.abc.Mapping[str, float] | None
        :param global_bonus: Bonus additif par défaut (échelle ``[0, 1]``).
        :type global_bonus: float
        :param global_penalty: Pénalité additive par défaut (échelle ``[0, 1]``).
        :type global_penalty: float

        :raises DeckEvaluationException: Si la configuration est invalide.
        """
        table = default_metric_weights() if weights is None else dict(weights)
        self._weight_items = _validate_and_sort_weights(table)
        self._default_bonus = _non_negative("global_bonus", global_bonus)
        self._default_penalty = _non_negative("global_penalty", global_penalty)

    @property
    def weight_items(self) -> tuple[tuple[str, float], ...]:
        """Poids triés ``(metric_id, poids)`` (copie logique immuable)."""
        return self._weight_items

    # pylint: disable=too-many-locals
    def aggregate(
        self,
        metrics: Sequence[DeckMetric],
        *,
        global_bonus: float | None = None,
        global_penalty: float | None = None,
    ) -> DeckEvaluation:
        """Produit une :class:`DeckEvaluation` complète.

        :param metrics: Métriques à combiner (``metric_id`` uniques).
        :type metrics: collections.abc.Sequence[DeckMetric]
        :param global_bonus: Surcharge du bonus ; ``None`` = valeur du constructeur.
        :type global_bonus: float | None
        :param global_penalty: Surcharge de la pénalité ; ``None`` = constructeur.
        :type global_penalty: float | None
        :returns: Évaluation avec score, breakdown et explication.
        :rtype: DeckEvaluation

        :raises DeckEvaluationException: Si une métrique pondérée manque ou si les
            ajustements sont incohérents.
        """
        bonus = (
            self._default_bonus
            if global_bonus is None
            else _non_negative("global_bonus", global_bonus)
        )
        penalty = (
            self._default_penalty
            if global_penalty is None
            else _non_negative("global_penalty", global_penalty)
        )

        metric_tuple = tuple(metrics)
        by_id = _metrics_by_id(metric_tuple)
        row_data, weighted_sum, total_weight = _weighted_rows_and_totals(
            self._weight_items,
            by_id,
        )
        weighted_average = weighted_sum / total_weight
        lines_tuple = tuple(
            DeckEvaluationBreakdownLine(
                metric_id=mid,
                display_name=name,
                weight=w,
                normalized_score=s,
                weighted_product=prod,
                share_of_weighted_sum=(prod / weighted_sum if weighted_sum > 0 else 0.0),
            )
            for mid, name, w, s, prod in row_data
        )
        breakdown = DeckEvaluationBreakdown(
            lines=lines_tuple,
            total_weight=total_weight,
            weighted_sum=weighted_sum,
            weighted_average=weighted_average,
        )
        raw_final = weighted_average + bonus - penalty
        final_score = _clamp01(raw_final)
        score = DeckScore(
            weighted_average=weighted_average,
            global_bonus=bonus,
            global_penalty=penalty,
            final_score=final_score,
            total_weight=total_weight,
        )
        explanation = _build_composition_explanation(
            breakdown=breakdown,
            score=score,
            raw_final_before_clamp=raw_final,
        )
        return DeckEvaluation(
            metrics=metric_tuple,
            score=score,
            breakdown=breakdown,
            explanation=explanation,
        )


def _build_composition_explanation(
    *,
    breakdown: DeckEvaluationBreakdown,
    score: DeckScore,
    raw_final_before_clamp: float,
) -> DeckEvaluationExplanation:
    parts: list[str] = [f"moyenne pondérée {score.weighted_average:.3f}"]
    if score.global_bonus:
        parts.append(f"bonus +{score.global_bonus:.3f}")
    if score.global_penalty:
        parts.append(f"pénalité −{score.global_penalty:.3f}")
    parts.append(f"agrégat brut {raw_final_before_clamp:.3f}")
    parts.append(f"score final {score.final_score:.3f}")
    summary = "Composition : " + ", ".join(parts) + "."

    detail_rows: list[str] = [
        f"Poids total actif : {breakdown.total_weight:.3f}.",
        f"Somme pondérée Σ(w×s) : {breakdown.weighted_sum:.3f}.",
    ]
    for ln in breakdown.lines:
        pct = 100.0 * ln.share_of_weighted_sum
        detail_rows.append(
            f"{ln.metric_id} : poids {ln.weight:.3f} × {ln.normalized_score:.3f} "
            f"= {ln.weighted_product:.3f} (~{pct:.1f}% de la somme pondérée)"
        )
    if raw_final_before_clamp != score.final_score:
        detail_rows.append("Le score brut dépassait [0, 1] : application du plafonnement (clamp).")

    return DeckEvaluationExplanation(
        title="Évaluation pondérée agrégée",
        summary=summary,
        details=tuple(detail_rows),
    )
