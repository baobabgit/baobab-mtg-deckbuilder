"""Tests for :class:`CardAnalyticProviderProtocol`."""

from baobab_mtg_deckbuilder.deck_statistics.card_analytic_profile import CardAnalyticProfile
from baobab_mtg_deckbuilder.deck_statistics.card_analytic_provider_protocol import (
    CardAnalyticProviderProtocol,
)
from tests.baobab_mtg_deckbuilder.deck_statistics.fake_card_analytic_provider import (
    FakeCardAnalyticProvider,
)


class TestCardAnalyticProviderProtocol:
    """Runtime structural checks."""

    def test_fake_provider_isinstance(self) -> None:
        """Fake provider matches the protocol at runtime."""
        provider = FakeCardAnalyticProvider(
            {
                "X": CardAnalyticProfile(
                    mana_value=0,
                    is_land=False,
                    color_identity=frozenset(),
                    type_categories=frozenset({"Creature"}),
                ),
            }
        )
        assert isinstance(provider, CardAnalyticProviderProtocol)
