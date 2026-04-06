"""Tests for :class:`CardPool`."""

import pytest

from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry
from baobab_mtg_deckbuilder.exceptions.deck_configuration_exception import (
    DeckConfigurationException,
)
from tests.baobab_mtg_deckbuilder.pool.fake_catalog_card_provider import (
    FakeCatalogCardProvider,
)
from tests.baobab_mtg_deckbuilder.pool.fake_collection_pool_provider import (
    FakeCollectionPoolProvider,
)


class TestCardPool:
    """Tests for merged pools and lookups."""

    def test_from_entries_theoretical_merge_sums_ints(self) -> None:
        """Duplicate oracle names merge by sum when bounded."""
        pool = CardPool.from_entries(
            (
                CardPoolEntry("Bolt", 2),
                CardPoolEntry("Bolt", 1),
            ),
            pool_kind="theoretical",
        )
        assert pool.is_theoretical is True
        assert pool.lookup("Bolt") == CardPoolEntry("Bolt", 3)

    def test_theoretical_none_dominates(self) -> None:
        """Any unbounded entry makes the merged row unbounded."""
        pool = CardPool.from_entries(
            (
                CardPoolEntry("Giant Growth", 2),
                CardPoolEntry("Giant Growth", None),
            ),
            pool_kind="theoretical",
        )
        assert pool.lookup("Giant Growth") == CardPoolEntry("Giant Growth", None)

    def test_from_entries_physical_merges_and_rejects_none(self) -> None:
        """Physical pools reject undefined quantities."""
        with pytest.raises(DeckConfigurationException):
            CardPool.from_entries(
                (CardPoolEntry("X", None),),
                pool_kind="physical",
            )

    def test_physical_merge_sums(self) -> None:
        """Owned copies add up."""
        pool = CardPool.from_entries(
            (
                CardPoolEntry("Bear", 1),
                CardPoolEntry("Bear", 2),
            ),
            pool_kind="physical",
        )
        assert pool.lookup("Bear") == CardPoolEntry("Bear", 3)

    def test_quantity_available_absent_is_zero(self) -> None:
        """Missing names yield quantity 0."""
        pool = CardPool.from_entries(
            (CardPoolEntry("Only", None),),
            pool_kind="theoretical",
        )
        assert pool.quantity_available("Missing") == 0

    def test_quantity_available_unbounded_is_none(self) -> None:
        """Unbounded entries report ``None``."""
        pool = CardPool.from_entries(
            (CardPoolEntry("Forest", None),),
            pool_kind="theoretical",
        )
        assert pool.quantity_available("Forest") is None

    def test_from_catalog_fake_provider(self) -> None:
        """Building from a fake catalogue provider."""
        provider = FakeCatalogCardProvider(
            (
                CardPoolEntry("Delver of Secrets", None),
                CardPoolEntry("Island", None),
            )
        )
        pool = CardPool.from_catalog(provider)
        assert pool.distinct_card_count == 2
        assert pool.lookup("Island") is not None

    def test_from_collection_fake_provider(self) -> None:
        """Building from a fake collection provider."""
        provider = FakeCollectionPoolProvider(
            (
                CardPoolEntry("Duress", 2),
                CardPoolEntry("Swamp", 20),
            )
        )
        pool = CardPool.from_collection(provider)
        assert pool.is_theoretical is False
        assert pool.quantity_available("Duress") == 2

    def test_physical_post_init_rejects_none_row(self) -> None:
        """Direct construction enforces physical invariants."""
        with pytest.raises(DeckConfigurationException):
            CardPool(
                is_theoretical=False,
                entries=(CardPoolEntry("Bad", None),),
            )

    def test_distinct_card_count(self) -> None:
        """Property counts merged rows."""
        pool = CardPool.from_entries(
            (CardPoolEntry("A", 1), CardPoolEntry("B", 2)),
            pool_kind="physical",
        )
        assert pool.distinct_card_count == 2
