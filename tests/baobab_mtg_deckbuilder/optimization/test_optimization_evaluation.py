"""Tests pour l'évaluation par défaut de l'optimisation."""

from baobab_mtg_deckbuilder.deck_statistics.card_analytic_profile import CardAnalyticProfile
from baobab_mtg_deckbuilder.optimization.optimization_evaluation import (
    default_optimization_evaluation,
)
from tests.baobab_mtg_deckbuilder.deck_statistics.fake_card_analytic_provider import (
    FakeCardAnalyticProvider,
)
from tests.baobab_mtg_deckbuilder.mutation.constructed_deck_factory import sixty_spell_deck


class TestDefaultOptimizationEvaluation:
    """Pipeline statistiques + agrégateur."""

    def test_returns_deck_evaluation_in_valid_range(self) -> None:
        """Score final dans ``[0, 1]`` pour un deck construit factice."""
        deck, _pool = sixty_spell_deck()
        profiles = {
            f"Spell {i:02d}": CardAnalyticProfile(
                mana_value=2,
                is_land=False,
                color_identity=frozenset({"R"}),
                type_categories=frozenset({"Instant"}),
            )
            for i in range(15)
        }
        provider = FakeCardAnalyticProvider(profiles)
        ev = default_optimization_evaluation(deck, provider)
        assert 0.0 <= ev.score.final_score <= 1.0
        assert len(ev.metrics) == 5
