"""Entrée d'un pool : identité oracle et disponibilité."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.exceptions.deck_validation_exception import (
    DeckValidationException,
)


@dataclass(frozen=True, slots=True)
class CardPoolEntry:
    """Décrit une carte présente dans un pool avec sa disponibilité.

    Le nom anglais Oracle aligne la clé métier sur
    :class:`~baobab_mtg_deckbuilder.deck.deck_card_entry.DeckCardEntry`.

    :param english_oracle_name: Nom anglais Oracle unique (normalisé par strip).
    :type english_oracle_name: str
    :param available_quantity: Nombre d'exemplaires disponibles, ou ``None`` pour une
        disponibilité **non bornée** dans le pool (typique d'un catalogue théorique :
        la limite vient alors du format / des règles de deck).
    :type available_quantity: int | None

    :raises DeckValidationException: Si le nom est vide après normalisation ou si la
        quantité est un entier strictement négatif.
    """

    english_oracle_name: str
    available_quantity: int | None

    def __post_init__(self) -> None:
        normalized = self.english_oracle_name.strip()
        if not normalized:
            raise DeckValidationException(
                "Le nom anglais Oracle du pool ne peut pas être vide après normalisation."
            )
        object.__setattr__(self, "english_oracle_name", normalized)
        if self.available_quantity is not None and self.available_quantity < 0:
            raise DeckValidationException(
                "La quantité disponible dans le pool ne peut pas être négative."
            )
