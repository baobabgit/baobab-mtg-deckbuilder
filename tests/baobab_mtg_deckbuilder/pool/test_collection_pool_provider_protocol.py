"""Tests for :class:`CollectionPoolProviderProtocol`."""

from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry
from baobab_mtg_deckbuilder.pool.collection_pool_provider_protocol import (
    CollectionPoolProviderProtocol,
)
from tests.baobab_mtg_deckbuilder.pool.fake_collection_pool_provider import (
    FakeCollectionPoolProvider,
)


class TestCollectionPoolProviderProtocol:
    """Runtime structural checks."""

    def test_fake_provider_isinstance(self) -> None:
        """Fake provider matches the protocol at runtime."""
        provider = FakeCollectionPoolProvider((CardPoolEntry("Mountain", 4),))
        assert isinstance(provider, CollectionPoolProviderProtocol)
