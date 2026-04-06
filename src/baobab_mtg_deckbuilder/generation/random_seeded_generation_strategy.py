"""Stratégie pseudo-aléatoire contrôlée par graine (mélanges reproductibles)."""

from __future__ import annotations

from baobab_mtg_deckbuilder.generation.deck_generation_request import DeckGenerationRequest
from baobab_mtg_deckbuilder.generation.deck_generation_result import DeckGenerationResult
from baobab_mtg_deckbuilder.generation.deck_generation_strategy import DeckGenerationStrategy
from baobab_mtg_deckbuilder.generation.uniform_deck_generation import run_uniform_generation


class RandomSeededGenerationStrategy(DeckGenerationStrategy):
    """Mélange non-bases et bases (Construit) ou le main entier (Limité) avec ``random.Random``.

    Chaque candidat utilise un générateur dérivé : même graine utilisateur ⇒ mêmes decks.
    """

    @property
    def strategy_key(self) -> str:
        return "random_seeded"

    def generate(self, request: DeckGenerationRequest) -> DeckGenerationResult:
        return run_uniform_generation(
            strategy_key=self.strategy_key,
            request=request,
            shuffle_nonbasics=True,
            shuffle_basics=True,
            nonbasic_priority="alphabetical",
            apply_list_rotation=False,
        )
