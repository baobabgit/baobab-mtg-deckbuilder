"""Tests pour :class:`ColorFixOperator`."""

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.deck_statistics.card_analytic_profile import CardAnalyticProfile
from baobab_mtg_deckbuilder.mutation.color_fix_operator import ColorFixOperator
from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)
from tests.baobab_mtg_deckbuilder.deck_statistics.fake_card_analytic_provider import (
    FakeCardAnalyticProvider,
)


class TestColorFixOperator:
    """Correction de couleur via profils analytiques."""

    def test_introduces_missing_color(self) -> None:
        """Remplace un sort rouge par un sort bleu disponible dans le pool."""
        fmt = ConstructedFormatDefinition()
        main_entries: list[DeckCardEntry] = []
        for i in range(14):
            main_entries.append(DeckCardEntry(f"Spell {i:02d}", 4))
        main_entries.append(DeckCardEntry("RedSpell", 4))
        deck = Deck.from_sections(DeckSection.main(tuple(main_entries)), DeckSection.sideboard(()))
        pool = CardPool.from_entries(
            tuple(CardPoolEntry(f"Spell {i:02d}", 4) for i in range(14))
            + (CardPoolEntry("RedSpell", 4), CardPoolEntry("BlueSpell", 4)),
            pool_kind="physical",
        )
        profiles = {
            f"Spell {i:02d}": CardAnalyticProfile(
                mana_value=2,
                is_land=False,
                color_identity=frozenset({"R"}),
                type_categories=frozenset({"Instant"}),
            )
            for i in range(14)
        }
        profiles["RedSpell"] = CardAnalyticProfile(
            mana_value=1,
            is_land=False,
            color_identity=frozenset({"R"}),
            type_categories=frozenset({"Sorcery"}),
        )
        profiles["BlueSpell"] = CardAnalyticProfile(
            mana_value=1,
            is_land=False,
            color_identity=frozenset({"U"}),
            type_categories=frozenset({"Instant"}),
        )
        provider = FakeCardAnalyticProvider(profiles)
        ctx = DeckMutationContext(
            deck=deck,
            format_definition=fmt,
            pool=pool,
            analytic_provider=provider,
        )
        result = ColorFixOperator("U").apply(ctx)
        assert result.validation_report_after.is_valid
        names = result.deck_after.summary().main_quantity_by_english_name
        assert names.get("BlueSpell", 0) >= 1
