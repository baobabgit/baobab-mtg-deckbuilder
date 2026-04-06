"""Résultat immuable des statistiques analytiques d'un deck."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class DeckStatisticsResult:  # pylint: disable=too-many-instance-attributes
    """Agrégats déterministes pour le main (et miroir optionnel pour le sideboard).

    Les cartes sans profil fournisseur sont comptées dans
    :py:attr:`main_profile_missing_quantity` (idem sideboard).

    :param main_spell_mana_curve: Histogramme des sorts non-terrain : clés ``0`` à
        :py:data:`~baobab_mtg_deckbuilder.deck_statistics.deck_statistics.MANA_CURVE_CAP`
        (dernier bac = coût >= ce seuil).
    :type main_spell_mana_curve: collections.abc.Mapping[int, int]
    :param main_spell_mana_value_unknown_quantity: Exemplaires de sorts reconnus mais
        sans CMC exploitable (:py:attr:`CardAnalyticProfile.mana_value` ``None`` ou
        valeur incohérente).
    :type main_spell_mana_value_unknown_quantity: int
    :param main_color_quantity_by_label: Quantités « pip » par couleur WUBRG, ``\"C\"``
        (incolore connu), ``\"?\"`` (couleur inconnue).
    :type main_color_quantity_by_label: collections.abc.Mapping[str, int]
    :param main_type_quantity_by_label: Quantités par catégorie de type ; ``\"?\"`` si inconnues.
    :type main_type_quantity_by_label: collections.abc.Mapping[str, int]
    :param main_land_quantity: Nombre total d'exemplaires de terrain dans le main.
    :type main_land_quantity: int
    :param main_quantity_by_english_name: Copies par nom anglais (main), aligné sur le deck.
    :type main_quantity_by_english_name: collections.abc.Mapping[str, int]
    :param main_profile_missing_quantity: Exemplaires sans profil fournisseur.
    :type main_profile_missing_quantity: int
    :param sideboard_spell_mana_curve: Idem sideboard (souvent vide en construit).
    :type sideboard_spell_mana_curve: collections.abc.Mapping[int, int]
    :param sideboard_spell_mana_value_unknown_quantity: Idem sideboard.
    :type sideboard_spell_mana_value_unknown_quantity: int
    :param sideboard_color_quantity_by_label: Idem sideboard.
    :type sideboard_color_quantity_by_label: collections.abc.Mapping[str, int]
    :param sideboard_type_quantity_by_label: Idem sideboard.
    :type sideboard_type_quantity_by_label: collections.abc.Mapping[str, int]
    :param sideboard_land_quantity: Idem sideboard.
    :type sideboard_land_quantity: int
    :param sideboard_quantity_by_english_name: Idem sideboard.
    :type sideboard_quantity_by_english_name: collections.abc.Mapping[str, int]
    :param sideboard_profile_missing_quantity: Idem sideboard.
    :type sideboard_profile_missing_quantity: int
    """

    main_spell_mana_curve: Mapping[int, int]
    main_spell_mana_value_unknown_quantity: int
    main_color_quantity_by_label: Mapping[str, int]
    main_type_quantity_by_label: Mapping[str, int]
    main_land_quantity: int
    main_quantity_by_english_name: Mapping[str, int]
    main_profile_missing_quantity: int
    sideboard_spell_mana_curve: Mapping[int, int]
    sideboard_spell_mana_value_unknown_quantity: int
    sideboard_color_quantity_by_label: Mapping[str, int]
    sideboard_type_quantity_by_label: Mapping[str, int]
    sideboard_land_quantity: int
    sideboard_quantity_by_english_name: Mapping[str, int]
    sideboard_profile_missing_quantity: int

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "main_spell_mana_curve",
            MappingProxyType(dict(self.main_spell_mana_curve)),
        )
        object.__setattr__(
            self,
            "main_color_quantity_by_label",
            MappingProxyType(dict(self.main_color_quantity_by_label)),
        )
        object.__setattr__(
            self,
            "main_type_quantity_by_label",
            MappingProxyType(dict(self.main_type_quantity_by_label)),
        )
        object.__setattr__(
            self,
            "main_quantity_by_english_name",
            MappingProxyType(dict(self.main_quantity_by_english_name)),
        )
        object.__setattr__(
            self,
            "sideboard_spell_mana_curve",
            MappingProxyType(dict(self.sideboard_spell_mana_curve)),
        )
        object.__setattr__(
            self,
            "sideboard_color_quantity_by_label",
            MappingProxyType(dict(self.sideboard_color_quantity_by_label)),
        )
        object.__setattr__(
            self,
            "sideboard_type_quantity_by_label",
            MappingProxyType(dict(self.sideboard_type_quantity_by_label)),
        )
        object.__setattr__(
            self,
            "sideboard_quantity_by_english_name",
            MappingProxyType(dict(self.sideboard_quantity_by_english_name)),
        )
