"""Stratégie gloutonne déterministe (ordre alphabétique + rotation des listes)."""

from __future__ import annotations

from baobab_mtg_deckbuilder.generation.deck_generation_request import DeckGenerationRequest
from baobab_mtg_deckbuilder.generation.deck_generation_result import DeckGenerationResult
from baobab_mtg_deckbuilder.generation.deck_generation_strategy import DeckGenerationStrategy
from baobab_mtg_deckbuilder.generation.uniform_deck_generation import run_uniform_generation


class GreedyGenerationStrategy(DeckGenerationStrategy):
    """Remplit le main par ordre alphabétique, sans mélange.

    La rotation cyclique des listes par indice de candidat permet d'obtenir plusieurs
    decks distincts tout en restant entièrement déterministe pour une requête donnée.
    """

    @property
    def strategy_key(self) -> str:
        return "greedy"

    def generate(self, request: DeckGenerationRequest) -> DeckGenerationResult:
        return run_uniform_generation(
            strategy_key=self.strategy_key,
            request=request,
            shuffle_nonbasics=False,
            shuffle_basics=False,
            nonbasic_priority="alphabetical",
            apply_list_rotation=True,
        )
