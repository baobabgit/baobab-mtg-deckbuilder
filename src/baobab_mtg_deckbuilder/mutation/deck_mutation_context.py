"""Contexte d'exécution partagé par les opérateurs de mutation."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck_statistics.card_analytic_provider_protocol import (
    CardAnalyticProviderProtocol,
)
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.validation.format_definition import FormatDefinition


@dataclass(frozen=True, slots=True)
class DeckMutationContext:
    """Paramètres d'entrée : deck courant, format, pool et options analytiques.

    :param deck: Deck à transformer.
    :type deck: Deck
    :param format_definition: Format utilisé pour la validation avant / après.
    :type format_definition: FormatDefinition
    :param pool: Disponibilité des cartes (collection ou catalogue).
    :type pool: CardPool
    :param random_seed: Graine pour tout tirage futur déterministe.
    :type random_seed: int
    :param analytic_provider: Profils carte pour les opérateurs couleur / type.
    :type analytic_provider: CardAnalyticProviderProtocol | None
    :param score_fn: Score scalaire optionnel pour estimer l'impact (benefit/neutral/degrade).
    :type score_fn: collections.abc.Callable[[Deck], float] | None
    """

    deck: Deck
    format_definition: FormatDefinition
    pool: CardPool
    random_seed: int = 0
    analytic_provider: CardAnalyticProviderProtocol | None = None
    score_fn: Callable[[Deck], float] | None = None
