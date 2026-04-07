"""Paramètres d'une campagne d'optimisation itérative."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck_statistics.card_analytic_provider_protocol import (
    CardAnalyticProviderProtocol,
)
from baobab_mtg_deckbuilder.evaluation.deck_evaluation import DeckEvaluation
from baobab_mtg_deckbuilder.exceptions.deck_optimization_exception import DeckOptimizationException
from baobab_mtg_deckbuilder.mutation.deck_mutation_operator import DeckMutationOperator
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.validation.format_definition import FormatDefinition


@dataclass(frozen=True, slots=True)
class DeckOptimizationRequest:
    """Entrées du moteur : decks initiaux, pool, opérateurs et critères d'arrêt.

    Fournir soit ``evaluate_deck`` (score externe), soit ``analytic_provider`` pour la
    pipeline d'évaluation par défaut (statistiques + agrégateur pondéré).

    :param format_definition: Format cible (validation des decks initiaux et successeurs).
    :type format_definition: FormatDefinition
    :param pool: Disponibilité des cartes pour les mutations.
    :type pool: CardPool
    :param initial_decks: Point(s) de départ (non vide).
    :type initial_decks: tuple[Deck, ...]
    :param mutation_operators: Opérateurs appliqués pour générer le voisinage.
    :type mutation_operators: tuple[DeckMutationOperator, ...]
    :param random_seed: Graine pour reproductibilité des mutations.
    :type random_seed: int
    :param max_iterations: Nombre maximal d'itérations externes de la stratégie.
    :type max_iterations: int
    :param stagnation_patience: Arrêt si le meilleur score global ne progresse pas pendant
        ce nombre d'itérations ; ``None`` désactive ce critère.
    :type stagnation_patience: int | None
    :param score_epsilon: Tolérance numérique pour comparer deux scores.
    :type score_epsilon: float
    :param beam_width: Largeur du faisceau (stratégie faisceau uniquement).
    :type beam_width: int
    :param analytic_provider: Profils carte pour l'évaluation par défaut.
    :type analytic_provider: CardAnalyticProviderProtocol | None
    :param evaluate_deck: Fonction de score complète ; prime sur ``analytic_provider`` si les
        deux sont fournis.
    :type evaluate_deck: collections.abc.Callable[[Deck], DeckEvaluation] | None

    :raises DeckOptimizationException: Si la configuration est incohérente.
    """

    format_definition: FormatDefinition
    pool: CardPool
    initial_decks: tuple[Deck, ...]
    mutation_operators: tuple[DeckMutationOperator, ...]
    random_seed: int = 0
    max_iterations: int = 50
    stagnation_patience: int | None = 3
    score_epsilon: float = 1e-9
    beam_width: int = 3
    analytic_provider: CardAnalyticProviderProtocol | None = None
    evaluate_deck: Callable[[Deck], DeckEvaluation] | None = None

    def __post_init__(self) -> None:
        if not self.initial_decks:
            raise DeckOptimizationException("Au moins un deck initial est requis.")
        if self.max_iterations < 1:
            raise DeckOptimizationException(
                f"max_iterations doit être >= 1 (reçu : {self.max_iterations})."
            )
        if not self.mutation_operators:
            raise DeckOptimizationException("Au moins un opérateur de mutation est requis.")
        if self.beam_width < 1:
            raise DeckOptimizationException(
                f"beam_width doit être >= 1 (reçu : {self.beam_width})."
            )
        if self.evaluate_deck is None and self.analytic_provider is None:
            raise DeckOptimizationException(
                "Fournir ``evaluate_deck`` ou ``analytic_provider`` pour noter les decks."
            )
