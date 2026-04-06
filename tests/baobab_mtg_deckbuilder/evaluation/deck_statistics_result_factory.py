"""Fabrique minimale de :class:`DeckStatisticsResult` pour les tests d'évaluation."""

from __future__ import annotations

from collections.abc import Mapping

from baobab_mtg_deckbuilder.deck_statistics.deck_statistics_result import DeckStatisticsResult


def deck_statistics_result(
    *,
    main_spell_mana_curve: Mapping[int, int] | None = None,
    main_spell_mana_value_unknown_quantity: int = 0,
    main_color_quantity_by_label: Mapping[str, int] | None = None,
    main_type_quantity_by_label: Mapping[str, int] | None = None,
    main_land_quantity: int = 0,
    main_quantity_by_english_name: Mapping[str, int] | None = None,
    main_profile_missing_quantity: int = 0,
    sideboard_spell_mana_curve: Mapping[int, int] | None = None,
    sideboard_spell_mana_value_unknown_quantity: int = 0,
    sideboard_color_quantity_by_label: Mapping[str, int] | None = None,
    sideboard_type_quantity_by_label: Mapping[str, int] | None = None,
    sideboard_land_quantity: int = 0,
    sideboard_quantity_by_english_name: Mapping[str, int] | None = None,
    sideboard_profile_missing_quantity: int = 0,
) -> DeckStatisticsResult:
    """Construit un résultat avec des valeurs par défaut."""
    return DeckStatisticsResult(
        main_spell_mana_curve=dict(main_spell_mana_curve or {}),
        main_spell_mana_value_unknown_quantity=main_spell_mana_value_unknown_quantity,
        main_color_quantity_by_label=dict(main_color_quantity_by_label or {}),
        main_type_quantity_by_label=dict(main_type_quantity_by_label or {}),
        main_land_quantity=main_land_quantity,
        main_quantity_by_english_name=dict(main_quantity_by_english_name or {}),
        main_profile_missing_quantity=main_profile_missing_quantity,
        sideboard_spell_mana_curve=dict(sideboard_spell_mana_curve or {}),
        sideboard_spell_mana_value_unknown_quantity=sideboard_spell_mana_value_unknown_quantity,
        sideboard_color_quantity_by_label=dict(sideboard_color_quantity_by_label or {}),
        sideboard_type_quantity_by_label=dict(sideboard_type_quantity_by_label or {}),
        sideboard_land_quantity=sideboard_land_quantity,
        sideboard_quantity_by_english_name=dict(sideboard_quantity_by_english_name or {}),
        sideboard_profile_missing_quantity=sideboard_profile_missing_quantity,
    )
