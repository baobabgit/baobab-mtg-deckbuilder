"""Stratégie guidée par contraintes de rareté relative dans le pool."""

from __future__ import annotations

from baobab_mtg_deckbuilder.generation.deck_generation_request import DeckGenerationRequest
from baobab_mtg_deckbuilder.generation.deck_generation_result import DeckGenerationResult
from baobab_mtg_deckbuilder.generation.deck_generation_strategy import DeckGenerationStrategy
from baobab_mtg_deckbuilder.generation.uniform_deck_generation import run_uniform_generation


class ConstrainedGenerationStrategy(DeckGenerationStrategy):
    """Priorise les cartes les plus rares du pool (quantité disponible croissante).

    Sans mélange : ordre déterministe ; rotation par candidat pour diversifier légèrement
    lorsque plusieurs decks sont demandés.
    """

    @property
    def strategy_key(self) -> str:
        return "constrained"

    def generate(self, request: DeckGenerationRequest) -> DeckGenerationResult:
        return run_uniform_generation(
            strategy_key=self.strategy_key,
            request=request,
            shuffle_nonbasics=False,
            shuffle_basics=False,
            nonbasic_priority="scarce_first",
            apply_list_rotation=True,
        )
