"""Issue unitaire produite par une règle de validation."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)


@dataclass(frozen=True, slots=True)
class DeckValidationIssue:
    """Message typé lié au contrôle d'un :class:`~baobab_mtg_deckbuilder.deck.deck.Deck`.

    :param severity: Niveau :class:`DeckValidationIssueSeverity`.
    :type severity: DeckValidationIssueSeverity
    :param code: Code machine stable (ex. ``CONSTRUCTED_MAIN_TOO_SMALL``).
    :type code: str
    :param message: Description lisible pour un humain ou un journal.
    :type message: str
    :param affected_entity: Entité concernée (nom de carte, ``main``, ``sideboard``, …).
    :type affected_entity: str | None
    :param suggestion: Piste de correction optionnelle.
    :type suggestion: str | None
    """

    severity: DeckValidationIssueSeverity
    code: str
    message: str
    affected_entity: str | None = None
    suggestion: str | None = None
