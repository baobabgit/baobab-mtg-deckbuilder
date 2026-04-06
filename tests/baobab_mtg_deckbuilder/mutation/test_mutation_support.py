"""Tests des utilitaires internes de mutation."""

from baobab_mtg_deckbuilder.mutation.mutation_support import classify_impact


class TestMutationSupport:
    """Fonctions pures de classification."""

    def test_classify_impact_beneficial(self) -> None:
        """Score qui monte → bénéfique."""
        assert classify_impact(0.0, 1.0) == "beneficial"

    def test_classify_impact_degrading(self) -> None:
        """Score qui baisse → dégradant."""
        assert classify_impact(1.0, 0.0) == "degrading"

    def test_classify_impact_neutral_missing_scores(self) -> None:
        """Sans scores, impact neutre par convention."""
        assert classify_impact(None, 1.0) == "neutral"
        assert classify_impact(1.0, None) == "neutral"

    def test_classify_impact_neutral_epsilon(self) -> None:
        """Variations infimes → neutre."""
        assert classify_impact(1.0, 1.0 + 1e-12) == "neutral"
