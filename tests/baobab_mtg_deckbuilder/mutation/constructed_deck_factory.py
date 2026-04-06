"""Fabrique minimale de decks construits valides pour les tests de mutation."""

from __future__ import annotations

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry


def sixty_spell_deck(*, extra_pool_names: tuple[str, ...] = ()) -> tuple[Deck, CardPool]:
    """60 sorts distincts × 4 exemplaires + pool étendu optionnel."""
    main_entries = tuple(DeckCardEntry(f"Spell {i:02d}", 4) for i in range(15))
    deck = Deck.from_sections(DeckSection.main(main_entries), DeckSection.sideboard(()))
    pool_entries: list[CardPoolEntry] = [CardPoolEntry(f"Spell {i:02d}", 4) for i in range(15)]
    for name in extra_pool_names:
        pool_entries.append(CardPoolEntry(name, 4))
    pool = CardPool.from_entries(tuple(pool_entries), pool_kind="physical")
    return deck, pool
