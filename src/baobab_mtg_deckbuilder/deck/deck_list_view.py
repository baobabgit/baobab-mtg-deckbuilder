"""Vue en lecture seule du deck (ordre d'affichage déterministe)."""

from dataclasses import dataclass

from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry


@dataclass(frozen=True, slots=True)
class DeckListView:
    """Projection triée des entrées main et sideboard pour affichage ou export.

    Les entrées sont triées par nom anglais (insensible à la casse, puis sensibilité
    pour stabilité), indépendamment de l'ordre d'insertion dans :class:`DeckSection`.

    :param main_entries: Lignes du main, déjà triées.
    :type main_entries: tuple[DeckCardEntry, ...]
    :param sideboard_entries: Lignes du sideboard, déjà triées.
    :type sideboard_entries: tuple[DeckCardEntry, ...]
    """

    main_entries: tuple[DeckCardEntry, ...]
    sideboard_entries: tuple[DeckCardEntry, ...]

    @staticmethod
    def sorted_entries(entries: tuple[DeckCardEntry, ...]) -> tuple[DeckCardEntry, ...]:
        """Retourne une copie triée des entrées (ordre déterministe).

        :param entries: Entrées sources.
        :type entries: tuple[DeckCardEntry, ...]
        :returns: Tuple trié.
        :rtype: tuple[DeckCardEntry, ...]
        """
        return tuple(sorted(entries, key=lambda e: (e.english_name.lower(), e.english_name)))
