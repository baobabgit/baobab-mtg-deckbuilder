"""Contrainte métier déclarative attachée à un format."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeckConstraint:
    """Description lisible d'une contrainte de format (documentation / UI).

    Les règles exécutables sont des :class:`DeckValidationRule` ; cette classe
    porte l'intention métier et des paramètres optionnels pour l'explicabilité.

    :param code: Identifiant stable (ex. ``MAIN_MIN_CARDS``).
    :type code: str
    :param summary: Texte court expliquant la contrainte.
    :type summary: str
    :param value: Valeur entière associée si pertinent (ex. seuil minimal).
    :type value: int | None
    """

    code: str
    summary: str
    value: int | None = None
