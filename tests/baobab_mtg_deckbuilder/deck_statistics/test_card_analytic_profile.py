"""Tests for :class:`CardAnalyticProfile`."""

from baobab_mtg_deckbuilder.deck_statistics.card_analytic_profile import CardAnalyticProfile


class TestCardAnalyticProfile:
    """Immutable profile container."""

    def test_instantiation(self) -> None:
        """Profiles are frozen value objects."""
        profile = CardAnalyticProfile(
            mana_value=3,
            is_land=False,
            color_identity=frozenset({"B"}),
            type_categories=frozenset({"Instant"}),
        )
        assert profile.mana_value == 3
