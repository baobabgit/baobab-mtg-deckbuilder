"""Deck complet : main + sideboard, vues et synthèses."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck_list_view import DeckListView
from baobab_mtg_deckbuilder.deck.deck_section import (
    MAIN_DECK_SECTION_ID,
    SIDEBOARD_SECTION_ID,
    DeckSection,
)
from baobab_mtg_deckbuilder.deck.deck_summary import DeckSummary
from baobab_mtg_deckbuilder.exceptions.deck_validation_exception import (
    DeckValidationException,
)


@dataclass(frozen=True, slots=True)
class Deck:
    """Deck immuable : une section main et une section sideboard.

    Le modèle couvre à la fois le **Construit** et le **Limité** : mêmes sections,
    contraintes de format étant appliquées ailleurs.

    :param main_section: Section dont l'identifiant doit être
        :py:data:`~baobab_mtg_deckbuilder.deck.deck_section.MAIN_DECK_SECTION_ID`.
    :type main_section: DeckSection
    :param sideboard_section: Section dont l'identifiant doit être
        :py:data:`~baobab_mtg_deckbuilder.deck.deck_section.SIDEBOARD_SECTION_ID`.
    :type sideboard_section: DeckSection

    :raises DeckValidationException: Si les identifiants de section ne correspondent pas
        au main et au sideboard attendus.
    """

    main_section: DeckSection
    sideboard_section: DeckSection

    def __post_init__(self) -> None:
        if self.main_section.identifier != MAIN_DECK_SECTION_ID:
            raise DeckValidationException(
                "La section principale doit porter l'identifiant 'main' "
                f"(reçu : {self.main_section.identifier!r})."
            )
        if self.sideboard_section.identifier != SIDEBOARD_SECTION_ID:
            raise DeckValidationException(
                "La section sideboard doit porter l'identifiant 'sideboard' "
                f"(reçu : {self.sideboard_section.identifier!r})."
            )

    @classmethod
    def from_sections(
        cls,
        main_section: DeckSection,
        sideboard_section: DeckSection,
    ) -> Deck:
        """Construit un :class:`Deck` à partir de deux :class:`DeckSection`.

        :param main_section: Section main validée.
        :type main_section: DeckSection
        :param sideboard_section: Section sideboard validée.
        :type sideboard_section: DeckSection
        :returns: Deck immuable.
        :rtype: Deck
        """
        return cls(main_section=main_section, sideboard_section=sideboard_section)

    @property
    def main_total_quantity(self) -> int:
        """Nombre total de cartes dans le main.

        :rtype: int
        """
        return self.main_section.total_quantity

    @property
    def sideboard_total_quantity(self) -> int:
        """Nombre total de cartes dans le sideboard.

        :rtype: int
        """
        return self.sideboard_section.total_quantity

    @property
    def total_quantity(self) -> int:
        """Nombre total de cartes (main + sideboard).

        :rtype: int
        """
        return self.main_total_quantity + self.sideboard_total_quantity

    def list_view(self) -> DeckListView:
        """Vue triée déterministe pour parcours ou affichage.

        :returns: Vue en lecture seule.
        :rtype: DeckListView
        """
        return DeckListView(
            main_entries=DeckListView.sorted_entries(self.main_section.entries),
            sideboard_entries=DeckListView.sorted_entries(self.sideboard_section.entries),
        )

    def summary(self) -> DeckSummary:
        """Agrégats (totaux, regroupements par nom anglais, cardinalités distinctes).

        :returns: Synthèse immuable.
        :rtype: DeckSummary
        """
        return DeckSummary.from_entry_sequences(
            self.main_section.entries,
            self.sideboard_section.entries,
        )
