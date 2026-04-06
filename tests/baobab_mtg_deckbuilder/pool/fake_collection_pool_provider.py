"""Fournisseur de collection factice pour les tests."""

from dataclasses import dataclass

from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry


@dataclass(frozen=True, slots=True)
class FakeCollectionPoolProvider:
    """Implémentation minimale de :class:`CollectionPoolProviderProtocol`."""

    _entries: tuple[CardPoolEntry, ...]

    def iter_owned_entries(self) -> tuple[CardPoolEntry, ...]:
        return self._entries
