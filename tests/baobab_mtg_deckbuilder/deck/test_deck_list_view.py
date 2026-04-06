"""Tests for :class:`DeckListView`."""

from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_list_view import DeckListView


class TestDeckListView:
    """Tests for deterministic sorted views."""

    def test_sorted_entries_orders_case_insensitive_then_lexicographic(self) -> None:
        """Sort key is ``(lower(name), name)`` for stable ordering."""
        entries = (
            DeckCardEntry("zebra", 1),
            DeckCardEntry("Alpha", 1),
            DeckCardEntry("alpha", 1),
        )
        sorted_entries = DeckListView.sorted_entries(entries)
        names = [e.english_name for e in sorted_entries]
        assert names == ["Alpha", "alpha", "zebra"]
