"""Ajoute ou retire un terrain de base unique dans le main."""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import Literal, TypeAlias

from baobab_mtg_deckbuilder.exceptions.deck_mutation_exception import DeckMutationException
from baobab_mtg_deckbuilder.mutation.deck_mutation import DeckMutation
from baobab_mtg_deckbuilder.mutation.deck_mutation_context import DeckMutationContext
from baobab_mtg_deckbuilder.mutation.deck_mutation_operator import DeckMutationOperator
from baobab_mtg_deckbuilder.mutation.deck_mutation_result import DeckMutationResult
from baobab_mtg_deckbuilder.mutation.mutation_support import (
    assert_main_at_least_minimum,
    assert_pool_covers_name,
    build_mutation_result,
    mutate_section_quantities,
)
from baobab_mtg_deckbuilder.validation.basic_land_oracle_names import (
    DEFAULT_BASIC_LAND_ORACLE_NAMES,
)

LandDelta: TypeAlias = Literal[-1, 1]


class AdjustLandCountOperator(DeckMutationOperator):
    """Ajuste de ±1 un terrain de base reconnu (liste MVP) dans le main."""

    def __init__(self, basic_land_oracle_name: str, delta: LandDelta) -> None:
        self._land_name = basic_land_oracle_name.strip()
        self._delta = delta
        if self._land_name not in DEFAULT_BASIC_LAND_ORACLE_NAMES:
            raise DeckMutationException(
                f"« {self._land_name} » n'est pas un terrain de base reconnu pour cette mutation."
            )

    @property
    def operator_id(self) -> str:
        return "adjust_land_count"

    def apply(self, context: DeckMutationContext) -> DeckMutationResult:
        deck_before = context.deck

        def _mutate(quantities: MutableMapping[str, int]) -> None:
            current = quantities.get(self._land_name, 0)
            if self._delta == 1:
                quantities[self._land_name] = current + 1
                return
            if current < 1:
                raise DeckMutationException(
                    f"Impossible de retirer un « {self._land_name} » : aucun exemplaire au main."
                )
            quantities[self._land_name] = current - 1
            if quantities[self._land_name] == 0:
                del quantities[self._land_name]

        deck_after = mutate_section_quantities(deck_before, "main", _mutate)
        assert_main_at_least_minimum(deck_after, context.format_definition)
        if self._delta == 1:
            assert_pool_covers_name(deck_after, context.pool, self._land_name)
        direction = "Ajout" if self._delta == 1 else "Retrait"
        mutation = DeckMutation(
            mutation_code="adjust_land_count",
            message=f"{direction} d'un « {self._land_name} » au main.",
            section_identifier="main",
        )
        justification = (
            f"{direction} d'un terrain de base pour ajuster la manabase "
            f"(delta {self._delta:+d})."
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
