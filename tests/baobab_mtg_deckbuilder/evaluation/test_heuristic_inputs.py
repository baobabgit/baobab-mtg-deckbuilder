"""Tests for heuristic input helpers."""

from baobab_mtg_deckbuilder.evaluation.heuristic_inputs import (
    main_deck_card_quantity,
    main_nonland_spell_quantity,
)
from tests.baobab_mtg_deckbuilder.evaluation.deck_statistics_result_factory import (
    deck_statistics_result,
)


class TestHeuristicInputs:
    """Derived quantities from statistics."""

    def test_main_deck_card_quantity(self) -> None:
        """Sums english-name quantities."""
        stats = deck_statistics_result(
            main_quantity_by_english_name={"A": 3, "B": 7},
        )
        assert main_deck_card_quantity(stats) == 10

    def test_main_nonland_spell_quantity(self) -> None:
        """Curve plus unknown mana count."""
        stats = deck_statistics_result(
            main_spell_mana_curve={1: 4, 2: 6},
            main_spell_mana_value_unknown_quantity=2,
        )
        assert main_nonland_spell_quantity(stats) == 12
