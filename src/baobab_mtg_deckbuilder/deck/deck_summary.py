"""Agrégats sur un deck (totaux et regroupements par nom anglais)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType

from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry


def _sum_by_english_name(entries: Sequence[DeckCardEntry]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry.english_name] = counts.get(entry.english_name, 0) + entry.quantity
    return dict(sorted(counts.items(), key=lambda item: (item[0].lower(), item[0])))


@dataclass(frozen=True, slots=True)
class DeckSummary:
    """Synthèse immuable : tailles, quantités et regroupements par nom Oracle anglais.

    Les dictionnaires exposés sont en lecture seule (:class:`types.MappingProxyType`).

    :param main_total_quantity: Nombre total de cartes dans le main.
    :type main_total_quantity: int
    :param sideboard_total_quantity: Nombre total de cartes dans le sideboard.
    :type sideboard_total_quantity: int
    :param total_quantity: Somme main + sideboard.
    :type total_quantity: int
    :param main_quantity_by_english_name: Quantités agrégées par nom anglais (main).
    :type main_quantity_by_english_name: collections.abc.Mapping[str, int]
    :param sideboard_quantity_by_english_name: Idem pour le sideboard.
    :type sideboard_quantity_by_english_name: collections.abc.Mapping[str, int]
    :param main_distinct_english_names: Nombre de noms anglais distincts (main).
    :type main_distinct_english_names: int
    :param sideboard_distinct_english_names: Nombre de noms anglais distincts (sideboard).
    :type sideboard_distinct_english_names: int
    """

    main_total_quantity: int
    sideboard_total_quantity: int
    total_quantity: int
    main_quantity_by_english_name: Mapping[str, int]
    sideboard_quantity_by_english_name: Mapping[str, int]
    main_distinct_english_names: int
    sideboard_distinct_english_names: int

    @classmethod
    def from_entry_sequences(
        cls,
        main_entries: Sequence[DeckCardEntry],
        sideboard_entries: Sequence[DeckCardEntry],
    ) -> DeckSummary:
        """Calcule les agrégats à partir des entrées main et sideboard.

        :param main_entries: Lignes du main.
        :type main_entries: collections.abc.Sequence[DeckCardEntry]
        :param sideboard_entries: Lignes du sideboard.
        :type sideboard_entries: collections.abc.Sequence[DeckCardEntry]
        :returns: Synthèse prête à l'emploi.
        :rtype: DeckSummary
        """
        main_map = _sum_by_english_name(main_entries)
        side_map = _sum_by_english_name(sideboard_entries)
        main_total = sum(main_map.values())
        side_total = sum(side_map.values())
        return cls(
            main_total_quantity=main_total,
            sideboard_total_quantity=side_total,
            total_quantity=main_total + side_total,
            main_quantity_by_english_name=MappingProxyType(main_map),
            sideboard_quantity_by_english_name=MappingProxyType(side_map),
            main_distinct_english_names=len(main_map),
            sideboard_distinct_english_names=len(side_map),
        )
