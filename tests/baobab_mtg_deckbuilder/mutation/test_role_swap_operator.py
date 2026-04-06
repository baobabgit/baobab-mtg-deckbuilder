"""Tests pour :class:`RoleSwapOperator`."""

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.mutation.role_swap_operator import RoleSwapOperator
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)


class TestRoleSwapOperator:
    """Échange main ↔ sideboard."""

    def test_swap_preserves_main_size(self) -> None:
        """Le main garde 60 cartes et le sideboard reste légal."""
        fmt = ConstructedFormatDefinition()
        main_entries = []
        for i in range(14):
            main_entries.append(DeckCardEntry(f"Spell {i:02d}", 4))
        main_entries.append(DeckCardEntry("Spell 14", 4))
        deck = Deck.from_sections(
            DeckSection.main(tuple(main_entries)),
            DeckSection.sideboard((DeckCardEntry("Spell 15", 1),)),
        )
        entries = [CardPoolEntry(f"Spell {i:02d}", 4) for i in range(15)]
        entries.append(CardPoolEntry("Spell 15", 4))
        pool = CardPool.from_entries(tuple(entries), pool_kind="physical")
        ctx = DeckMutationContext(deck=deck, format_definition=fmt, pool=pool)
        result = RoleSwapOperator("Spell 13", "Spell 15").apply(ctx)
        assert result.deck_after.main_total_quantity == 60
        assert result.validation_report_after.is_valid
        side = result.deck_after.summary().sideboard_quantity_by_english_name
        assert side.get("Spell 13", 0) >= 1
        main = result.deck_after.summary().main_quantity_by_english_name
        assert main.get("Spell 15", 0) >= 1
