"""Boucle de génération à paramètres constants pour toute la requête."""

from __future__ import annotations

from baobab_mtg_deckbuilder.generation.deck_candidate import DeckCandidate
from baobab_mtg_deckbuilder.generation.deck_generation_request import DeckGenerationRequest
from baobab_mtg_deckbuilder.generation.deck_generation_result import DeckGenerationResult
from baobab_mtg_deckbuilder.generation.deck_generation_strategy import DeckGenerationStrategy
from baobab_mtg_deckbuilder.generation.maindeck_from_pool_builder import (
    CardPriority,
    build_maindeck_candidate,
)


def run_uniform_generation(
    *,
    strategy_key: str,
    request: DeckGenerationRequest,
    shuffle_nonbasics: bool,
    shuffle_basics: bool,
    nonbasic_priority: CardPriority,
    apply_list_rotation: bool,
) -> DeckGenerationResult:
    """Produit des candidats avec les mêmes options de builder pour chaque indice.

    :param strategy_key: Identifiant de la stratégie appelante.
    :type strategy_key: str
    :param request: Requête utilisateur.
    :type request: DeckGenerationRequest
    :param shuffle_nonbasics: Mélange des non-bases (Construit) ou cartes (Limité).
    :type shuffle_nonbasics: bool
    :param shuffle_basics: Mélange des bases (Construit).
    :type shuffle_basics: bool
    :param nonbasic_priority: Ordre avant mélange ou rotation.
    :type nonbasic_priority: CardPriority
    :param apply_list_rotation: Rotation cyclique sans mélange.
    :type apply_list_rotation: bool
    :returns: Résultat agrégé.
    :rtype: DeckGenerationResult
    """
    candidates: list[DeckCandidate] = []
    for index in range(request.candidate_count):
        deck = build_maindeck_candidate(
            request.pool,
            request.format_definition,
            rng=DeckGenerationStrategy.rng_for_candidate(request.random_seed, index),
            shuffle_nonbasics=shuffle_nonbasics,
            shuffle_basics=shuffle_basics,
            nonbasic_priority=nonbasic_priority,
            candidate_index=index,
            apply_list_rotation=apply_list_rotation,
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
        strategy_key=strategy_key,
        request=request,
        candidates=tuple(candidates),
    )
