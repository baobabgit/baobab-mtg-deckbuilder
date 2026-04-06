"""Combinaison simple : candidats pairs gloutons, impairs aléatoires (graine)."""

from __future__ import annotations

from baobab_mtg_deckbuilder.generation.deck_candidate import DeckCandidate
from baobab_mtg_deckbuilder.generation.deck_generation_request import DeckGenerationRequest
from baobab_mtg_deckbuilder.generation.deck_generation_result import DeckGenerationResult
from baobab_mtg_deckbuilder.generation.deck_generation_strategy import DeckGenerationStrategy
from baobab_mtg_deckbuilder.generation.maindeck_from_pool_builder import build_maindeck_candidate


class HybridGenerationStrategy(DeckGenerationStrategy):
    """Pour chaque indice ``i``, utilise le mode glouton si ``i`` est pair, sinon aléatoire."""

    @property
    def strategy_key(self) -> str:
        return "hybrid"

    def generate(self, request: DeckGenerationRequest) -> DeckGenerationResult:
        candidates: list[DeckCandidate] = []
        for index in range(request.candidate_count):
            rng = self.rng_for_candidate(request.random_seed, index)
            use_shuffle = index % 2 == 1
            deck = build_maindeck_candidate(
                request.pool,
                request.format_definition,
                rng=rng,
                shuffle_nonbasics=use_shuffle,
                shuffle_basics=use_shuffle,
                nonbasic_priority="alphabetical",
                candidate_index=index,
                apply_list_rotation=not use_shuffle,
            )
            report = request.format_definition.validate(deck)
            candidates.append(
                DeckCandidate(
                    candidate_index=index,
                    deck=deck,
                    validation_report=report,
                )
            )
        return DeckGenerationResult(
            strategy_key=self.strategy_key,
            request=request,
            candidates=tuple(candidates),
        )
