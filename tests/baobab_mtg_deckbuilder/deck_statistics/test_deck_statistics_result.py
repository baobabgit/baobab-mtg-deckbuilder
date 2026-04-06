"""Tests for :class:`DeckStatisticsResult`."""

import pytest

from baobab_mtg_deckbuilder.deck_statistics.deck_statistics_result import DeckStatisticsResult


class TestDeckStatisticsResult:
    """Immutability of result mappings."""

    def test_mappings_are_read_only(self) -> None:
        """Histograms are exposed as mapping proxies."""
        result = DeckStatisticsResult(
            main_spell_mana_curve={1: 2},
            main_spell_mana_value_unknown_quantity=0,
            main_color_quantity_by_label={"R": 2},
            main_type_quantity_by_label={"Instant": 2},
            main_land_quantity=0,
            main_quantity_by_english_name={"Shock": 2},
            main_profile_missing_quantity=0,
            sideboard_spell_mana_curve={},
            sideboard_spell_mana_value_unknown_quantity=0,
            sideboard_color_quantity_by_label={},
            sideboard_type_quantity_by_label={},
            sideboard_land_quantity=0,
            sideboard_quantity_by_english_name={},
            sideboard_profile_missing_quantity=0,
        )
        with pytest.raises(TypeError):
            result.main_spell_mana_curve[2] = 1  # type: ignore[index]
