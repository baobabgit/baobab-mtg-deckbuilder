"""Suggestion explicable de remplacement de carte (entrée métier des opérateurs)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from baobab_mtg_deckbuilder.exceptions.deck_mutation_exception import DeckMutationException

SectionChoice: TypeAlias = Literal["main", "sideboard"]


@dataclass(frozen=True, slots=True)
class DeckReplacementSuggestion:
    """Décrit un remplacement ciblé : retrait d'un nom et ajout d'un autre.

    :param remove_english_name: Nom Oracle anglais à retirer.
    :type remove_english_name: str
    :param add_english_name: Nom Oracle anglais à ajouter.
    :type add_english_name: str
    :param section_identifier: Section touchée (``main`` ou ``sideboard``).
    :type section_identifier: SectionChoice
    :param copies: Nombre d'exemplaires déplacés (>= 1).
    :type copies: int
    :param rationale: Justification métier ou heuristique.
    :type rationale: str
    """

    remove_english_name: str
    add_english_name: str
    section_identifier: SectionChoice
    copies: int
    rationale: str

    def __post_init__(self) -> None:
        if self.copies < 1:
            raise DeckMutationException(
                f"Le nombre de copies pour un remplacement doit être >= 1 (reçu : {self.copies})."
            )
