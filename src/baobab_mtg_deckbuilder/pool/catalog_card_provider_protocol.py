"""Protocole d'accès à un catalogue de cartes (pool théorique)."""

from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable

from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry


@runtime_checkable
class CatalogCardProviderProtocol(Protocol):
    """Fournit les entrées d'un **catalogue** (cartes légales / connues sans stock).

    Les implémentations restent hors de cette librairie (fichiers, API distante, etc.) ;
    seul ce contrat structurel est requis pour construire un :class:`CardPool` théorique.

    Les entrées retournées ont en général ``available_quantity is None`` (non borné
    dans le pool ; les plafonds viennent du format).
    """

    def iter_theoretical_entries(self) -> Sequence[CardPoolEntry]:
        """Retourne une séquence déterministe d'entrées catalogue.

        :returns: Cartes offertes par le catalogue pour la construction / génération.
        :rtype: collections.abc.Sequence[CardPoolEntry]
        """
