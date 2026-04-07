"""État d'un candidat dans la recherche (deck + évaluation)."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.evaluation.deck_evaluation import DeckEvaluation


@dataclass(frozen=True, slots=True)
class DeckSearchState:
    """Couple deck / score agrégé pour le moteur d'optimisation.

    :param deck: Liste courante (main + sideboard).
    :type deck: Deck
    :param evaluation: Évaluation heuristique (ex. agrégation pondérée).
    :type evaluation: DeckEvaluation
    """

    deck: Deck
    evaluation: DeckEvaluation

    @property
    def score_value(self) -> float:
        """Raccourci vers le score final normalisé ``[0, 1]``."""
        return self.evaluation.score.final_score
