"""Gravité d'un point de contrôle dans un rapport de validation."""

from enum import StrEnum


class DeckValidationIssueSeverity(StrEnum):
    """Niveau de sévérité d'une :class:`DeckValidationIssue`.

    Les **erreurs** invalident le deck au sens du format ; les **avertissements**
    signalent un risque ou une ambiguïté ; les **infos** documentent le contexte.
    """

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
