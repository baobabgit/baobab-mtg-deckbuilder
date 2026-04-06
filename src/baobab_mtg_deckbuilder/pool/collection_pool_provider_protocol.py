"""Protocole d'accès à une collection physique (pool réel)."""

from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable

from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry


@runtime_checkable
class CollectionPoolProviderProtocol(Protocol):
    """Fournit les entrées d'une **collection** (exemplaires réellement possédés).

    Aucune hypothèse n'est faite sur le stockage ; le fournisseur agrège simplement
    des :class:`CardPoolEntry` avec quantités entières ``>= 0``.
    """

    def iter_owned_entries(self) -> Sequence[CardPoolEntry]:
        """Retourne une séquence déterministe d'entrées de collection.

        :returns: Cartes possédées et quantités disponibles pour deckbuilding.
        :rtype: collections.abc.Sequence[CardPoolEntry]
        """
