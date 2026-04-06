"""Profil analytique minimal pour une carte (courbe, couleurs, types, terrain)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CardAnalyticProfile:
    """Données déclaratives pour agréger les statistiques d'un deck.

    Toutes les informations sont **optionnelles** au niveau des champs : une valeur
    ``None`` ou un ensemble vide signale une information **inconnue** pour la métrique
    correspondante (voir
    :class:`~baobab_mtg_deckbuilder.deck_statistics.deck_statistics.DeckStatistics`).

    :param mana_value: Coût converti (CMC) pour la courbe de mana des sorts ;
        ``None`` si inconnu (hors courbe, compteur dédié).
    :type mana_value: int | None
    :param is_land: Indique si la carte est un terrain ; ``None`` si inconnu.
    :type is_land: bool | None
    :param color_identity: Couleurs WUBRG (par ex. ``\"W\"``, ``\"U\"``, …) ; vide si inconnu
        ou sans identité de couleur connue.
    :type color_identity: frozenset[str]
    :param type_categories: Libellés de types (ex. ``\"Creature\"``, ``\"Land\"``) ;
        vide si inconnu.
    :type type_categories: frozenset[str]
    """

    mana_value: int | None
    is_land: bool | None
    color_identity: frozenset[str]
    type_categories: frozenset[str]
