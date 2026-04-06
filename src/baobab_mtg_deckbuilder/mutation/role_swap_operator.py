"""Échange un exemplaire main → sideboard contre un exemplaire sideboard → main."""

from __future__ import annotations

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.exceptions.deck_mutation_exception import DeckMutationException
from baobab_mtg_deckbuilder.mutation.deck_mutation import DeckMutation
from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.mutation.deck_mutation_operator import DeckMutationOperator
from baobab_mtg_deckbuilder.mutation.deck_mutation_result import DeckMutationResult
from baobab_mtg_deckbuilder.mutation.mutation_support import (
    assert_constructed_nonbasic_cap,
    build_mutation_result,
    counts_map,
    map_to_sorted_entries,
)


class RoleSwapOperator(DeckMutationOperator):
    """Permute des rôles de decklist : une carte descend du main, une autre monte du side."""

    def __init__(self, main_to_side_name: str, side_to_main_name: str) -> None:
        self._main_to_side = main_to_side_name.strip()
        self._side_to_main = side_to_main_name.strip()
        if not self._main_to_side or not self._side_to_main:
            raise DeckMutationException(
                "Les noms Oracle pour l'échange de rôle ne peuvent pas être vides."
            )

    @property
    def operator_id(self) -> str:
        return "role_swap"

    def apply(self, context: DeckMutationContext) -> DeckMutationResult:
        deck_before = context.deck
        main_q = dict(counts_map(deck_before.main_section.entries))
        side_q = dict(counts_map(deck_before.sideboard_section.entries))
        if main_q.get(self._main_to_side, 0) < 1:
            raise DeckMutationException(
                f"« {self._main_to_side} » n'est pas présente au main pour être descendue."
            )
        if side_q.get(self._side_to_main, 0) < 1:
            raise DeckMutationException(
                f"« {self._side_to_main} » n'est pas présente au sideboard pour monter."
            )
        main_q[self._main_to_side] -= 1
        if main_q[self._main_to_side] == 0:
            del main_q[self._main_to_side]
        side_q[self._main_to_side] = side_q.get(self._main_to_side, 0) + 1

        side_q[self._side_to_main] -= 1
        if side_q[self._side_to_main] == 0:
            del side_q[self._side_to_main]
        main_q[self._side_to_main] = main_q.get(self._side_to_main, 0) + 1

        deck_after = Deck.from_sections(
            DeckSection.main(map_to_sorted_entries(main_q)),
            DeckSection.sideboard(map_to_sorted_entries(side_q)),
        )
        assert_constructed_nonbasic_cap(deck_after, context.format_definition)
        mutation = DeckMutation(
            mutation_code="role_swap",
            message=(
                f"Échange : « {self._main_to_side} » vers le sideboard, "
                f"« {self._side_to_main} » vers le main."
            ),
            section_identifier="main",
        )
        justification = (
            "Permutation contrôlée entre main et sideboard pour réaffecter des rôles "
            "(pré- / post-sideboard)."
        )
        return build_mutation_result(
            operator_id=self.operator_id,
            deck_before=deck_before,
            deck_after=deck_after,
            mutations_applied=(mutation,),
            justification=justification,
            format_definition=context.format_definition,
            score_fn=context.score_fn,
        )
