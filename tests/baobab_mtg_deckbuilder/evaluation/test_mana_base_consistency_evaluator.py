"""Tests for :class:`ManaBaseConsistencyEvaluator`."""

from baobab_mtg_deckbuilder.evaluation.mana_base_consistency_evaluator import (
    ManaBaseConsistencyEvaluator,
)
from tests.baobab_mtg_deckbuilder.evaluation.deck_statistics_result_factory import (
    deck_statistics_result,
)


class TestManaBaseConsistencyEvaluator:
    """Cohérence des données."""

    def test_favorable_complete_data(self) -> None:
        """Pas de lacunes → score proche du maximum."""
        stats = deck_statistics_result(
            main_quantity_by_english_name={"A": 40},
            main_spell_mana_curve={2: 40},
            main_color_quantity_by_label={"R": 40},
            main_type_quantity_by_label={"Creature": 40},
        )
        metric = ManaBaseConsistencyEvaluator().evaluate(stats)
        assert metric.normalized_score == 1.0
        assert "1.00" in metric.explanation.summary

    def test_unfavorable_missing_profiles(self) -> None:
        """Profils manquants partiels → pénalisation."""
        good = ManaBaseConsistencyEvaluator().evaluate(
            deck_statistics_result(
                main_quantity_by_english_name={"A": 40},
                main_spell_mana_curve={1: 40},
                main_color_quantity_by_label={"W": 40},
            )
        )
        bad = ManaBaseConsistencyEvaluator().evaluate(
            deck_statistics_result(
                main_quantity_by_english_name={"A": 40},
                main_spell_mana_curve={1: 20},
                main_profile_missing_quantity=20,
                main_color_quantity_by_label={"W": 40},
            )
        )
        assert bad.normalized_score < good.normalized_score

    def test_unfavorable_unknown_color_pips(self) -> None:
        """Les pips « ? » réduisent le score."""
        base = deck_statistics_result(
            main_quantity_by_english_name={"A": 20},
            main_spell_mana_curve={1: 20},
            main_color_quantity_by_label={"U": 20},
        )
        with_q = deck_statistics_result(
            main_quantity_by_english_name={"A": 20},
            main_spell_mana_curve={1: 20},
            main_color_quantity_by_label={"U": 10, "?": 10},
        )
        m_base = ManaBaseConsistencyEvaluator().evaluate(base)
        m_q = ManaBaseConsistencyEvaluator().evaluate(with_q)
        assert m_q.normalized_score < m_base.normalized_score

    def test_explanation_lists_factors(self) -> None:
        """Le résumé contient les trois facteurs multiplicatifs."""
        stats = deck_statistics_result(
            main_quantity_by_english_name={"A": 10},
            main_spell_mana_curve={1: 8},
            main_spell_mana_value_unknown_quantity=2,
            main_color_quantity_by_label={"B": 9, "?": 1},
            main_profile_missing_quantity=1,
        )
        metric = ManaBaseConsistencyEvaluator().evaluate(stats)
        assert "profils" in metric.explanation.summary.lower()
        assert len(metric.explanation.details) == 3
