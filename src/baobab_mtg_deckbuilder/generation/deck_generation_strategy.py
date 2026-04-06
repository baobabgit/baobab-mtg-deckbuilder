"""Stratégie abstraite de génération de decks."""

from __future__ import annotations

import random
from abc import ABC, abstractmethod

from baobab_mtg_deckbuilder.generation.deck_generation_request import DeckGenerationRequest
from baobab_mtg_deckbuilder.generation.deck_generation_result import DeckGenerationResult


class DeckGenerationStrategy(ABC):
    """Contrat des stratégies : transformer une requête en :class:`DeckGenerationResult`."""

    @property
    @abstractmethod
    def strategy_key(self) -> str:
        """Clé stable (logs, comparaisons, sérialisation)."""

    @abstractmethod
    def generate(self, request: DeckGenerationRequest) -> DeckGenerationResult:
        """Produit ``request.candidate_count`` candidats typés et validés.

        :param request: Paramètres de génération.
        :type request: DeckGenerationRequest
        :returns: Résultat immuable.
        :rtype: DeckGenerationResult
        """

    @staticmethod
    def rng_for_candidate(random_seed: int, candidate_index: int) -> random.Random:
        """Générateur dérivé par candidat (évite des séries corrélées trop proches).

        :param random_seed: Graine utilisateur.
        :type random_seed: int
        :param candidate_index: Indice du candidat.
        :type candidate_index: int
        :returns: Instance isolée pour ce candidat.
        :rtype: random.Random
        """
        derived = (random_seed * 1_000_003) ^ (candidate_index * 97_531)
        return random.Random(
            derived
        )  # nosec B311  # reproductibilité deck, hors usage cryptographique
