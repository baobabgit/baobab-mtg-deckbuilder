"""Résultat agrégé d'une génération de decks candidats."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.generation.deck_candidate import DeckCandidate
from baobab_mtg_deckbuilder.generation.deck_generation_request import DeckGenerationRequest


@dataclass(frozen=True, slots=True)
class DeckGenerationResult:
    """Sortie structurée d'une stratégie : plusieurs :class:`DeckCandidate`.

    :param strategy_key: Identifiant stable de la stratégie ayant produit ces candidats.
    :type strategy_key: str
    :param request: Requête d'origine (traçabilité, reproductibilité).
    :type request: DeckGenerationRequest
    :param candidates: Candidats dans l'ordre croissant des indices.
    :type candidates: tuple[DeckCandidate, ...]
    """

    strategy_key: str
    request: DeckGenerationRequest
    candidates: tuple[DeckCandidate, ...]
