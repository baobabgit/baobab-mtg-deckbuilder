"""Rapport agrégé des issues de validation."""

from __future__ import annotations

from dataclasses import dataclass

from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)


def _severity_rank(severity: DeckValidationIssueSeverity) -> int:
    order = (
        DeckValidationIssueSeverity.ERROR,
        DeckValidationIssueSeverity.WARNING,
        DeckValidationIssueSeverity.INFO,
    )
    return order.index(severity)


@dataclass(frozen=True, slots=True)
class DeckValidationReport:
    """Synthèse déterministe des :class:`DeckValidationIssue` pour un deck.

    L'ordre des issues est figé : gravité (erreur, avertissement, info), puis
    ``code``, puis ``message``, puis entité affectée.

    :param issues: Liste immuable des problèmes détectés.
    :type issues: tuple[DeckValidationIssue, ...]
    """

    issues: tuple[DeckValidationIssue, ...]

    @classmethod
    def from_issues(cls, issues: tuple[DeckValidationIssue, ...]) -> DeckValidationReport:
        """Construit un rapport en triant les issues de façon déterministe.

        :param issues: Issues brutes (ordre quelconque).
        :type issues: tuple[DeckValidationIssue, ...]
        :returns: Rapport trié.
        :rtype: DeckValidationReport
        """
        sorted_issues = tuple(
            sorted(
                issues,
                key=lambda i: (
                    _severity_rank(i.severity),
                    i.code,
                    i.message,
                    i.affected_entity or "",
                ),
            )
        )
        return cls(issues=sorted_issues)

    @property
    def error_count(self) -> int:
        """Nombre d'issues de gravité ``error``."""
        return sum(1 for i in self.issues if i.severity == DeckValidationIssueSeverity.ERROR)

    @property
    def warning_count(self) -> int:
        """Nombre d'issues de gravité ``warning``."""
        return sum(1 for i in self.issues if i.severity == DeckValidationIssueSeverity.WARNING)

    @property
    def info_count(self) -> int:
        """Nombre d'issues de gravité ``info``."""
        return sum(1 for i in self.issues if i.severity == DeckValidationIssueSeverity.INFO)

    @property
    def is_valid(self) -> bool:
        """Vrai si aucune erreur bloquante n'est présente (avertissements / infos permis)."""
        return self.error_count == 0
