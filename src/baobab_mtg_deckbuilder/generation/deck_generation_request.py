"""Requête de génération de decks candidats."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.exceptions.deck_generation_exception import DeckGenerationException
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.validation.format_definition import FormatDefinition


@dataclass(frozen=True, slots=True)
class DeckGenerationRequest:
    """Paramètres d'entrée pour produire plusieurs decks depuis un pool.

    :param format_definition: Format cible (validation exécutée sur chaque candidat).
    :type format_definition: FormatDefinition
    :param pool: Cartes disponibles (réel ou théorique).
    :type pool: CardPool
    :param random_seed: Graine pour reproductibilité des stratégies aléatoires ou hybrides.
    :type random_seed: int
    :param candidate_count: Nombre de candidats à produire (>= 1).
    :type candidate_count: int

    :raises DeckGenerationException: Si ``candidate_count`` est invalide ou le pool est vide.
    """

    format_definition: FormatDefinition
    pool: CardPool
    random_seed: int
    candidate_count: int

    def __post_init__(self) -> None:
        if self.candidate_count < 1:
            raise DeckGenerationException(
                f"Le paramètre candidate_count doit être >= 1 (reçu : {self.candidate_count})."
            )
        if not self.pool.entries:
            raise DeckGenerationException("Le pool ne contient aucune carte exploitable.")
