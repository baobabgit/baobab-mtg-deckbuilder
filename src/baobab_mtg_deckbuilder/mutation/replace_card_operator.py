"""Remplace des exemplaires d'une carte par une autre dans une section."""

from __future__ import annotations

from baobab_mtg_deckbuilder.exceptions.deck_mutation_exception import DeckMutationException
from baobab_mtg_deckbuilder.mutation.deck_mutation import DeckMutation
from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.mutation.deck_mutation_operator import DeckMutationOperator
from baobab_mtg_deckbuilder.mutation.deck_mutation_result import DeckMutationResult
from baobab_mtg_deckbuilder.mutation.deck_replacement_suggestion import DeckReplacementSuggestion
from baobab_mtg_deckbuilder.mutation.mutation_support import (
    assert_constructed_nonbasic_cap,
    assert_main_at_least_minimum,
    assert_pool_covers_name,
    build_mutation_result,
    counts_map,
    map_to_sorted_entries,
    section_entries,
    with_replaced_section,
)


class ReplaceCardOperator(DeckMutationOperator):
    """Applique une :class:`DeckReplacementSuggestion` dans une section donnée."""

    def __init__(self, suggestion: DeckReplacementSuggestion) -> None:
        self._suggestion = suggestion

    @property
    def operator_id(self) -> str:
        return "replace_card"

    def apply(self, context: DeckMutationContext) -> DeckMutationResult:
        suggestion = self._suggestion
        deck_before = context.deck
        section = suggestion.section_identifier
        quantities = dict(counts_map(section_entries(deck_before, section)))
        available_remove = quantities.get(suggestion.remove_english_name, 0)
        if available_remove < suggestion.copies:
            raise DeckMutationException(
                f"Impossible de retirer {suggestion.copies} exemplaire(s) de "
                f"« {suggestion.remove_english_name} » dans {section} "
                f"(présent : {available_remove})."
            )
        quantities[suggestion.remove_english_name] -= suggestion.copies
        if quantities[suggestion.remove_english_name] == 0:
            del quantities[suggestion.remove_english_name]
        quantities[suggestion.add_english_name] = (
            quantities.get(suggestion.add_english_name, 0) + suggestion.copies
        )
        new_entries = map_to_sorted_entries(quantities)
        deck_after = with_replaced_section(deck_before, section, new_entries)
        assert_main_at_least_minimum(deck_after, context.format_definition)
        assert_pool_covers_name(deck_after, context.pool, suggestion.add_english_name)
        assert_constructed_nonbasic_cap(deck_after, context.format_definition)
        mutation = DeckMutation(
            mutation_code="replace_card",
            message=(
                f"Remplacement de {suggestion.copies}× « {suggestion.remove_english_name} » "
                f"par « {suggestion.add_english_name} » dans {section}."
            ),
            section_identifier=section,
        )
        return build_mutation_result(
            operator_id=self.operator_id,
            deck_before=deck_before,
            deck_after=deck_after,
            mutations_applied=(mutation,),
            justification=suggestion.rationale,
            format_definition=context.format_definition,
            score_fn=context.score_fn,
        )
