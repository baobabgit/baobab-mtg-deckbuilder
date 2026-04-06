"""Tests pour :class:`AdjustLandCountOperator`."""

import pytest

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.exceptions.deck_mutation_exception import DeckMutationException
from baobab_mtg_deckbuilder.mutation.adjust_land_count_operator import AdjustLandCountOperator
from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)


class TestAdjustLandCountOperator:
    """Ajustement ±1 d'un terrain de base."""

    def test_unknown_basic_raises(self) -> None:
        """Seuls les terrains de base reconnus MVP sont acceptés à la construction."""
        with pytest.raises(DeckMutationException, match="terrain de base"):
            AdjustLandCountOperator("Volcanic Island", 1)

    def _deck_with_lands_and_spells(self) -> tuple[Deck, CardPool]:
        spells = tuple(DeckCardEntry(f"Spell {i:02d}", 4) for i in range(10))
        lands = (DeckCardEntry("Mountain", 22),)
        deck = Deck.from_sections(DeckSection.main(spells + lands), DeckSection.sideboard(()))
        entries = [CardPoolEntry(f"Spell {i:02d}", 4) for i in range(10)]
        entries.append(CardPoolEntry("Mountain", 30))
        entries.append(CardPoolEntry("Island", 30))
        pool = CardPool.from_entries(tuple(entries), pool_kind="physical")
        return deck, pool

    def test_add_basic_land(self) -> None:
        """Ajout d'une île reproductible et traçable."""
        fmt = ConstructedFormatDefinition()
        deck, pool = self._deck_with_lands_and_spells()
        ctx = DeckMutationContext(deck=deck, format_definition=fmt, pool=pool)
        result = AdjustLandCountOperator("Island", 1).apply(ctx)
        assert result.validation_report_after.is_valid
        assert result.deck_after.main_total_quantity == deck.main_total_quantity + 1
        summary = result.deck_after.summary()
        assert summary.main_quantity_by_english_name.get("Island", 0) == 1

    def test_remove_basic_land(self) -> None:
        """Retrait d'une montagne lorsque le minimum main reste respecté."""
        fmt = ConstructedFormatDefinition()
        deck, pool = self._deck_with_lands_and_spells()
        ctx = DeckMutationContext(deck=deck, format_definition=fmt, pool=pool)
        result = AdjustLandCountOperator("Mountain", -1).apply(ctx)
        assert result.validation_report_after.is_valid
        assert result.deck_after.main_total_quantity == deck.main_total_quantity - 1
