"""Ligne de deck : nom oracle anglais et quantité."""

from dataclasses import dataclass

from baobab_mtg_deckbuilder.exceptions.deck_validation_exception import (
    DeckValidationException,
)


@dataclass(frozen=True, slots=True)
class DeckCardEntry:
    """Représente une ligne de deck (même nom oracle, quantité donnée).

    Le champ :py:attr:`english_name` sert de **clé métier** pour agréger les
    quantités (Construit ou Limité). Il doit correspondre au nom anglais Oracle
    unique, normalisé (espaces en tête/fin supprimés).

    :param english_name: Nom anglais Oracle de la carte.
    :type english_name: str
    :param quantity: Nombre d'exemplaires pour cette ligne (>= 1).
    :type quantity: int

    :raises DeckValidationException: Si le nom est vide après normalisation ou
        si la quantité est strictement négative ou nulle.
    """

    english_name: str
    quantity: int

    def __post_init__(self) -> None:
        normalized = self.english_name.strip()
        if not normalized:
            raise DeckValidationException(
                "Le nom anglais (oracle) ne peut pas être vide après normalisation."
            )
        object.__setattr__(self, "english_name", normalized)
        if self.quantity < 1:
            raise DeckValidationException("La quantité doit être un entier >= 1.")
