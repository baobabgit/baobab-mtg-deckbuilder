"""Tests for :class:`CatalogCardProviderProtocol`."""

from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry
from baobab_mtg_deckbuilder.pool.catalog_card_provider_protocol import (
    CatalogCardProviderProtocol,
)
from tests.baobab_mtg_deckbuilder.pool.fake_catalog_card_provider import (
    FakeCatalogCardProvider,
)


class TestCatalogCardProviderProtocol:
    """Runtime structural checks."""

    def test_fake_provider_isinstance(self) -> None:
        """Fake provider matches the protocol at runtime."""
        provider = FakeCatalogCardProvider((CardPoolEntry("Plains", None),))
        assert isinstance(provider, CatalogCardProviderProtocol)
