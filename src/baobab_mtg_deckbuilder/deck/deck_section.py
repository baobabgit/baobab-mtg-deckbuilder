"""Section de deck (principal ou sideboard)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.exceptions.deck_validation_exception import (
    DeckValidationException,
)

MAIN_DECK_SECTION_ID: Final[str] = "main"
"""Identifiant stable de la section main deck (Construit / Limité)."""

SIDEBOARD_SECTION_ID: Final[str] = "sideboard"
"""Identifiant stable de la section sideboard."""


@dataclass(frozen=True, slots=True)
class DeckSection:
    """Ensemble immuable d'entrées appartenant à une section nommée.

    Les identifiants standard :py:data:`MAIN_DECK_SECTION_ID` et
    :py:data:`SIDEBOARD_SECTION_ID` couvrent les formats Construit et Limité.
    D'autres identifiants pourront être introduits plus tard (ex. zones
    supplémentaires) sans changer ce type.

    :param identifier: Clé stable de la section (ex. ``main``, ``sideboard``).
    :type identifier: str
    :param entries: Lignes de cartes dans l'ordre logique choisi par l'appelant.
    :type entries: tuple[DeckCardEntry, ...]

    :raises DeckValidationException: Si l'identifiant est vide après normalisation.
    """

    identifier: str
    entries: tuple[DeckCardEntry, ...]

    def __post_init__(self) -> None:
        ident = self.identifier.strip()
        if not ident:
            raise DeckValidationException(
                "L'identifiant de section ne peut pas être vide après normalisation."
            )
        object.__setattr__(self, "identifier", ident)

    @classmethod
    def main(cls, entries: Sequence[DeckCardEntry]) -> DeckSection:
        """Construit la section main deck.

        :param entries: Lignes du main.
        :type entries: collections.abc.Sequence[DeckCardEntry]
        :returns: Section marquée :py:data:`MAIN_DECK_SECTION_ID`.
        :rtype: DeckSection
        """
        return cls(MAIN_DECK_SECTION_ID, tuple(entries))

    @classmethod
    def sideboard(cls, entries: Sequence[DeckCardEntry]) -> DeckSection:
        """Construit la section sideboard.

        :param entries: Lignes du sideboard (souvent vide en Limited avant construction).
        :type entries: collections.abc.Sequence[DeckCardEntry]
        :returns: Section marquée :py:data:`SIDEBOARD_SECTION_ID`.
        :rtype: DeckSection
        """
        return cls(SIDEBOARD_SECTION_ID, tuple(entries))

    @property
    def total_quantity(self) -> int:
        """Somme des quantités des entrées de cette section.

        :returns: Nombre total de cartes dans la section.
        :rtype: int
        """
        return sum(entry.quantity for entry in self.entries)
