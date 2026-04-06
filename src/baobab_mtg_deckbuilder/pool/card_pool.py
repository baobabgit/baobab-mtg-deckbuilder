"""Pool de cartes : vue théorique (catalogue) ou réelle (collection)."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Literal, Sequence, cast

from baobab_mtg_deckbuilder.exceptions.deck_configuration_exception import (
    DeckConfigurationException,
)
from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry
from baobab_mtg_deckbuilder.pool.catalog_card_provider_protocol import (
    CatalogCardProviderProtocol,
)
from baobab_mtg_deckbuilder.pool.collection_pool_provider_protocol import (
    CollectionPoolProviderProtocol,
)


def _merge_entries_theoretical(entries: Sequence[CardPoolEntry]) -> tuple[CardPoolEntry, ...]:
    """Fusionne par nom Oracle : ``None`` domine (disponibilité non bornée)."""
    by_name: dict[str, int | None] = {}
    for entry in entries:
        name = entry.english_oracle_name
        qty = entry.available_quantity
        if qty is None:
            by_name[name] = None
            continue
        if name not in by_name:
            by_name[name] = qty
        elif by_name[name] is None:
            continue
        else:
            previous = cast(int, by_name[name])
            by_name[name] = previous + qty
    ordered = sorted(by_name.items(), key=lambda item: (item[0].lower(), item[0]))
    return tuple(CardPoolEntry(n, q) for n, q in ordered)


def _merge_entries_physical(entries: Sequence[CardPoolEntry]) -> tuple[CardPoolEntry, ...]:
    """Fusionne par nom Oracle en sommant les quantités entières."""
    sums: defaultdict[str, int] = defaultdict(int)
    for entry in entries:
        if entry.available_quantity is None:
            raise DeckConfigurationException(
                "Une entrée de collection ne peut pas avoir une quantité indéfinie "
                f"({entry.english_oracle_name!r})."
            )
        sums[entry.english_oracle_name] += entry.available_quantity
    ordered = sorted(sums.items(), key=lambda item: (item[0].lower(), item[0]))
    return tuple(CardPoolEntry(n, q) for n, q in ordered)


@dataclass(frozen=True, slots=True)
class CardPool:
    """Vue immuable d'un pool pour génération et validation.

    * **Théorique** (:py:attr:`is_theoretical` ``True``) : dérivé d'un catalogue ;
      les quantités ``None`` signifient l'absence de plafond **dans le pool**.
    * **Réel** (:py:attr:`is_theoretical` ``False``) : dérivé d'une collection ;
      toutes les quantités sont des entiers ``>= 0``.

    :param is_theoretical: ``True`` si le pool représente un catalogue, ``False`` si collection.
    :type is_theoretical: bool
    :param entries: Entrées fusionnées et triées par nom Oracle.
    :type entries: tuple[CardPoolEntry, ...]

    :raises DeckConfigurationException: Si un pool réel contient une quantité ``None``.
    """

    is_theoretical: bool
    entries: tuple[CardPoolEntry, ...]

    def __post_init__(self) -> None:
        if not self.is_theoretical:
            for entry in self.entries:
                if entry.available_quantity is None:
                    raise DeckConfigurationException(
                        "Un pool réel ne peut contenir d'entrée à quantité indéfinie "
                        f"({entry.english_oracle_name!r})."
                    )

    @classmethod
    def from_catalog(cls, provider: CatalogCardProviderProtocol) -> CardPool:
        """Construit un pool théorique à partir d'un fournisseur catalogue.

        :param provider: Source catalogue respectant :class:`CatalogCardProviderProtocol`.
        :type provider: CatalogCardProviderProtocol
        :returns: Pool fusionné et trié.
        :rtype: CardPool
        """
        merged = _merge_entries_theoretical(tuple(provider.iter_theoretical_entries()))
        return cls(is_theoretical=True, entries=merged)

    @classmethod
    def from_collection(cls, provider: CollectionPoolProviderProtocol) -> CardPool:
        """Construit un pool réel à partir d'un fournisseur de collection.

        :param provider: Source collection respectant :class:`CollectionPoolProviderProtocol`.
        :type provider: CollectionPoolProviderProtocol
        :returns: Pool fusionné et trié.
        :rtype: CardPool
        """
        merged = _merge_entries_physical(tuple(provider.iter_owned_entries()))
        return cls(is_theoretical=False, entries=merged)

    @classmethod
    def from_entries(
        cls,
        entries: Sequence[CardPoolEntry],
        *,
        pool_kind: Literal["theoretical", "physical"],
    ) -> CardPool:
        """Construit un pool à partir d'entrées brutes (tests ou adaptateurs).

        :param entries: Lignes à fusionner.
        :type entries: collections.abc.Sequence[CardPoolEntry]
        :param pool_kind: ``theoretical`` ou ``physical``.
        :type pool_kind: typing.Literal['theoretical', 'physical']
        :returns: Pool normalisé.
        :rtype: CardPool
        """
        if pool_kind == "theoretical":
            merged = _merge_entries_theoretical(tuple(entries))
            return cls(is_theoretical=True, entries=merged)
        merged = _merge_entries_physical(tuple(entries))
        return cls(is_theoretical=False, entries=merged)

    def lookup(self, english_oracle_name: str) -> CardPoolEntry | None:
        """Retourne l'entrée du pool pour ce nom Oracle, ou ``None`` si absente.

        :param english_oracle_name: Nom recherché (strip appliqué).
        :type english_oracle_name: str
        :returns: Entrée fusionnée ou ``None``.
        :rtype: CardPoolEntry | None
        """
        key = english_oracle_name.strip()
        for entry in self.entries:
            if entry.english_oracle_name == key:
                return entry
        return None

    def quantity_available(self, english_oracle_name: str) -> int | None:
        """Quantité disponible : ``None`` si non bornée, entier si plafonnée, ``0`` si absente.

        Pour une carte absente du pool théorique, retourne ``0`` (hors catalogue).
        Pour une carte absente du pool réel, retourne ``0`` (non possédée).

        :param english_oracle_name: Nom Oracle anglais.
        :type english_oracle_name: str
        :rtype: int | None
        """
        entry = self.lookup(english_oracle_name)
        if entry is None:
            return 0
        return entry.available_quantity

    @property
    def distinct_card_count(self) -> int:
        """Nombre de noms Oracle distincts dans le pool."""
        return len(self.entries)
