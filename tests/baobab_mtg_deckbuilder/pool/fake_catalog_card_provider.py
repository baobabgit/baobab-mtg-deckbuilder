"""Fournisseur catalogue factice pour les tests."""

from dataclasses import dataclass

from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry


@dataclass(frozen=True, slots=True)
class FakeCatalogCardProvider:
    """Implémentation minimale de :class:`CatalogCardProviderProtocol`."""

    _entries: tuple[CardPoolEntry, ...]

    def iter_theoretical_entries(self) -> tuple[CardPoolEntry, ...]:
        return self._entries
