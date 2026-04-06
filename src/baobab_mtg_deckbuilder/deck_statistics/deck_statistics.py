"""Statistiques analytiques pour un :class:`~baobab_mtg_deckbuilder.deck.deck.Deck`."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_summary import DeckSummary
from baobab_mtg_deckbuilder.deck_statistics.card_analytic_profile import CardAnalyticProfile
from baobab_mtg_deckbuilder.deck_statistics.card_analytic_provider_protocol import (
    CardAnalyticProviderProtocol,
)
from baobab_mtg_deckbuilder.deck_statistics.deck_statistics_result import DeckStatisticsResult

MANA_CURVE_CAP: int = 7
"""Dernier indice de la courbe de mana : regroupe les coûts ``>= MANA_CURVE_CAP``."""

_COLOR_ORDER: tuple[str, ...] = ("W", "U", "B", "R", "G", "C", "?")


def _is_land_card(profile: CardAnalyticProfile) -> bool:
    """Détermine si le profil décrit un terrain (règles déterministes documentées)."""
    if profile.is_land is True:
        return True
    if profile.is_land is False:
        return False
    return "Land" in profile.type_categories


def _sort_str_keys(counts: Mapping[str, int]) -> dict[str, int]:
    ordered: dict[str, int] = {}
    for label in _COLOR_ORDER:
        value = counts.get(label, 0)
        if value:
            ordered[label] = value
    remaining = [(key, value) for key, value in counts.items() if key not in ordered and value]
    remaining.sort(key=lambda item: (item[0].lower(), item[0]))
    ordered.update(dict(remaining))
    return ordered


def _sort_type_keys(counts: Mapping[str, int]) -> dict[str, int]:
    return dict(sorted(counts.items(), key=lambda item: (item[0].lower(), item[0])))


def _sort_mana_keys(counts: Mapping[int, int]) -> dict[int, int]:
    return dict(sorted(counts.items()))


def _analyze_entries(  # pylint: disable=too-many-locals,too-many-branches
    entries: Sequence[DeckCardEntry],
    provider: CardAnalyticProviderProtocol | None,
) -> tuple[
    dict[int, int],
    int,
    dict[str, int],
    dict[str, int],
    int,
    dict[str, int],
    int,
]:
    """Agrège une séquence de lignes (une section)."""
    quantity_by_name: dict[str, int] = {}
    for entry in entries:
        quantity_by_name[entry.english_name] = (
            quantity_by_name.get(entry.english_name, 0) + entry.quantity
        )
    quantity_by_name = dict(
        sorted(quantity_by_name.items(), key=lambda item: (item[0].lower(), item[0]))
    )

    spell_curve: defaultdict[int, int] = defaultdict(int)
    mana_unknown = 0
    color_counts: defaultdict[str, int] = defaultdict(int)
    type_counts: defaultdict[str, int] = defaultdict(int)
    land_qty = 0
    profile_missing = 0

    for name, qty in quantity_by_name.items():
        if provider is None:
            profile_missing += qty
            continue
        profile = provider.analytic_profile_for(name)
        if profile is None:
            profile_missing += qty
            continue

        if _is_land_card(profile):
            land_qty += qty
        else:
            if profile.mana_value is None:
                mana_unknown += qty
            else:
                mv = profile.mana_value
                if mv < 0:
                    mana_unknown += qty
                else:
                    bucket = mv if mv < MANA_CURVE_CAP else MANA_CURVE_CAP
                    spell_curve[bucket] += qty

        if profile.color_identity:
            for color in profile.color_identity:
                color_counts[color] += qty
        else:
            color_counts["?"] += qty

        if profile.type_categories:
            for label in profile.type_categories:
                type_counts[label] += qty
        else:
            type_counts["?"] += qty

    return (
        _sort_mana_keys(spell_curve),
        mana_unknown,
        _sort_str_keys(color_counts),
        _sort_type_keys(type_counts),
        land_qty,
        quantity_by_name,
        profile_missing,
    )


class DeckStatistics:
    """Point d'entrée pour les agrégats analytiques (découplé des stratégies d'optimisation)."""

    @staticmethod
    def analyze(
        deck: Deck,
        provider: CardAnalyticProviderProtocol | None = None,
    ) -> DeckStatisticsResult:
        """Calcule les statistiques pour le main et le sideboard.

        **Terrain** : :py:func:`_is_land_card` — ``is_land`` si renseigné, sinon présence
        du libellé ``\"Land\"`` dans :py:attr:`CardAnalyticProfile.type_categories`.

        **Courbe de mana** : uniquement les cartes non-terrain avec ``mana_value >= 0`` ;
        les coûts ``>=`` :py:data:`MANA_CURVE_CAP` sont regroupés dans ce bac.

        **Couleurs** : chaque exemplaire contribue une fois par couleur dans
        :py:attr:`CardAnalyticProfile.color_identity` ; identité vide → ``\"?\"``.

        **Types** : chaque exemplaire contribue une fois par libellé dans
        :py:attr:`CardAnalyticProfile.type_categories` ; ensemble vide → ``\"?\"``.

        :param deck: Deck à analyser.
        :type deck: Deck
        :param provider: Source de profils ; ``None`` équivaut à l'absence totale de métadonnées.
        :type provider: CardAnalyticProviderProtocol | None
        :returns: Résultat immuable.
        :rtype: DeckStatisticsResult
        """
        summary = DeckSummary.from_entry_sequences(
            deck.main_section.entries,
            deck.sideboard_section.entries,
        )
        main_block = _analyze_entries(deck.main_section.entries, provider)
        side_block = _analyze_entries(deck.sideboard_section.entries, provider)

        return DeckStatisticsResult(
            main_spell_mana_curve=main_block[0],
            main_spell_mana_value_unknown_quantity=main_block[1],
            main_color_quantity_by_label=main_block[2],
            main_type_quantity_by_label=main_block[3],
            main_land_quantity=main_block[4],
            main_quantity_by_english_name=dict(summary.main_quantity_by_english_name),
            main_profile_missing_quantity=main_block[6],
            sideboard_spell_mana_curve=side_block[0],
            sideboard_spell_mana_value_unknown_quantity=side_block[1],
            sideboard_color_quantity_by_label=side_block[2],
            sideboard_type_quantity_by_label=side_block[3],
            sideboard_land_quantity=side_block[4],
            sideboard_quantity_by_english_name=dict(summary.sideboard_quantity_by_english_name),
            sideboard_profile_missing_quantity=side_block[6],
        )
