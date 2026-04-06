"""Évaluateur heuristique : cohérence des données de mana (profils, CMC, couleurs)."""

from __future__ import annotations

from baobab_mtg_deckbuilder.deck_statistics.deck_statistics_result import DeckStatisticsResult
from baobab_mtg_deckbuilder.evaluation.deck_evaluation_explanation import (
    DeckEvaluationExplanation,
)
from baobab_mtg_deckbuilder.evaluation.deck_metric import DeckMetric
from baobab_mtg_deckbuilder.evaluation.heuristic_inputs import (
    main_deck_card_quantity,
    main_nonland_spell_quantity,
)


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


class ManaBaseConsistencyEvaluator:
    """Agrège des pénalités sur l'incertitude analytique (pas le moteur de règles).

    Facteurs multiplicatifs dans ``[0, 1]`` puis clamp :

    * ``1 - min(1, profils_manquants / taille_main)``
    * ``1 - min(1, pips_? / max(1, pips_couleur_total))``
    * ``1 - min(1, CMC_inconnu / max(1, sorts_non_terrain))``

    Interprétation : données complètes → 1,0 ; lacunes fortes → tend vers 0.
    """

    METRIC_ID: str = "mana_data_consistency"
    DISPLAY_NAME: str = "Cohérence des données de mana"

    # pylint: disable=too-many-locals
    def evaluate(self, stats: DeckStatisticsResult) -> DeckMetric:
        """Calcule la métrique de cohérence.

        :param stats: Agrégats du deck.
        :type stats: DeckStatisticsResult
        :returns: Métrique avec explication.
        :rtype: DeckMetric
        """
        main_size = max(main_deck_card_quantity(stats), 1)
        missing = stats.main_profile_missing_quantity
        f_missing = 1.0 - min(1.0, missing / main_size)

        color_total = sum(stats.main_color_quantity_by_label.values())
        unknown_color = stats.main_color_quantity_by_label.get("?", 0)
        denom_color = max(color_total, 1)
        f_color = 1.0 - min(1.0, unknown_color / denom_color)

        spells = main_nonland_spell_quantity(stats)
        denom_spell = max(spells, 1)
        unknown_mana = stats.main_spell_mana_value_unknown_quantity
        f_mana = 1.0 - min(1.0, unknown_mana / denom_spell) if spells > 0 else 1.0

        normalized = _clamp01(f_missing * f_color * f_mana)
        raw = 100.0 * normalized

        summary = (
            f"Cohérence agrégée {normalized:.2f} "
            f"(profils {f_missing:.2f} × couleurs {f_color:.2f} × CMC {f_mana:.2f})."
        )
        details = (
            f"Profils manquants : {missing} / {main_size}.",
            f"Pips « ? » : {unknown_color} / {denom_color} pips totaux.",
            f"CMC inconnu : {unknown_mana} / {denom_spell} sorts non-terrain.",
        )
        explanation = DeckEvaluationExplanation(
            title=self.DISPLAY_NAME,
            summary=summary,
            details=details,
        )
        return DeckMetric(
            metric_id=self.METRIC_ID,
            display_name=self.DISPLAY_NAME,
            raw_score=raw,
            normalized_score=normalized,
            explanation=explanation,
        )
