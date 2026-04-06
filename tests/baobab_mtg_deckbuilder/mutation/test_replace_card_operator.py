"""Tests pour :class:`ReplaceCardOperator`."""

from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.mutation.deck_replacement_suggestion import DeckReplacementSuggestion
from baobab_mtg_deckbuilder.mutation.replace_card_operator import ReplaceCardOperator
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)
from tests.baobab_mtg_deckbuilder.mutation.constructed_deck_factory import sixty_spell_deck


class TestReplaceCardOperator:
    """Remplacement contrôlé dans le main."""

    def test_replace_keeps_constructed_valid(self) -> None:
        """Le deck reste valide après remplacement 1:1 dans le main."""
        fmt = ConstructedFormatDefinition()
        deck, pool = sixty_spell_deck(extra_pool_names=("ExtraSpell",))
        ctx = DeckMutationContext(deck=deck, format_definition=fmt, pool=pool)
        suggestion = DeckReplacementSuggestion(
            remove_english_name="Spell 00",
            add_english_name="ExtraSpell",
            section_identifier="main",
            copies=1,
            rationale="Tester un remplacement simple.",
        )
        result = ReplaceCardOperator(suggestion).apply(ctx)
        assert result.validation_report_before.is_valid
        assert result.validation_report_after.is_valid
        assert result.deck_before is deck
        assert result.deck_after.main_total_quantity == 60
        assert result.mutations_applied[0].mutation_code == "replace_card"
        assert "ExtraSpell" in result.mutations_applied[0].message
