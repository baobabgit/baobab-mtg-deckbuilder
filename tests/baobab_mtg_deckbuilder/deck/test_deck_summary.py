"""Tests for :class:`DeckSummary`."""

from types import MappingProxyType

from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_summary import DeckSummary


class TestDeckSummary:
    """Tests for aggregation by English oracle name."""

    def test_merges_duplicate_english_names(self) -> None:
        """Several lines with the same oracle name sum into one bucket."""
        main = (
            DeckCardEntry("Lightning Bolt", 2),
            DeckCardEntry("Lightning Bolt", 1),
        )
        summary = DeckSummary.from_entry_sequences(main, ())
        assert summary.main_quantity_by_english_name["Lightning Bolt"] == 3
        assert summary.main_total_quantity == 3
        assert summary.main_distinct_english_names == 1

    def test_sideboard_separate_from_main(self) -> None:
        """Sideboard counts do not mix with main aggregates."""
        main = (DeckCardEntry("Duress", 2),)
        side = (DeckCardEntry("Duress", 1),)
        summary = DeckSummary.from_entry_sequences(main, side)
        assert summary.main_quantity_by_english_name["Duress"] == 2
        assert summary.sideboard_quantity_by_english_name["Duress"] == 1
        assert summary.total_quantity == 3
        assert summary.sideboard_distinct_english_names == 1

    def test_mappings_are_read_only_proxy(self) -> None:
        """Quantity maps are :class:`types.MappingProxyType` instances."""
        summary = DeckSummary.from_entry_sequences(
            (DeckCardEntry("Card", 1),),
            (),
        )
        assert isinstance(summary.main_quantity_by_english_name, MappingProxyType)
        assert isinstance(summary.sideboard_quantity_by_english_name, MappingProxyType)
