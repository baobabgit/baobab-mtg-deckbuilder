"""Ensemble immuable de contraintes déclaratives."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.validation.deck_constraint import DeckConstraint


@dataclass(frozen=True, slots=True)
class DeckConstraintSet:
    """Regroupe des :class:`DeckConstraint` pour un même format logique.

    :param format_key: Clé du format (ex. ``constructed_mvp``).
    :type format_key: str
    :param constraints: Contraintes exposées aux consommateurs (ordre stable).
    :type constraints: tuple[DeckConstraint, ...]
    """

    format_key: str
    constraints: tuple[DeckConstraint, ...]
