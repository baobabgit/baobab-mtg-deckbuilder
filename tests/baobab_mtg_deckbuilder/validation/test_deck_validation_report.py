"""Tests for :class:`DeckValidationReport`."""

from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)
from baobab_mtg_deckbuilder.validation.deck_validation_report import DeckValidationReport


class TestDeckValidationReport:
    """Tests for aggregated reports."""

    def test_from_issues_sorts_by_severity_then_code(self) -> None:
        """Issues are ordered error, warning, info, then code."""
        issues = (
            DeckValidationIssue(
                severity=DeckValidationIssueSeverity.INFO,
                code="Z",
                message="z",
            ),
            DeckValidationIssue(
                severity=DeckValidationIssueSeverity.ERROR,
                code="A",
                message="a",
            ),
            DeckValidationIssue(
                severity=DeckValidationIssueSeverity.WARNING,
                code="M",
                message="m",
            ),
        )
        report = DeckValidationReport.from_issues(issues)
        severities = [i.severity for i in report.issues]
        assert severities == [
            DeckValidationIssueSeverity.ERROR,
            DeckValidationIssueSeverity.WARNING,
            DeckValidationIssueSeverity.INFO,
        ]

    def test_counts_and_is_valid(self) -> None:
        """Counts per severity; valid iff zero errors."""
        report = DeckValidationReport.from_issues(
            (
                DeckValidationIssue(
                    severity=DeckValidationIssueSeverity.ERROR,
                    code="E",
                    message="e",
                ),
                DeckValidationIssue(
                    severity=DeckValidationIssueSeverity.WARNING,
                    code="W",
                    message="w",
                ),
                DeckValidationIssue(
                    severity=DeckValidationIssueSeverity.INFO,
                    code="I",
                    message="i",
                ),
            )
        )
        assert report.error_count == 1
        assert report.warning_count == 1
        assert report.info_count == 1
        assert report.is_valid is False

    def test_is_valid_without_errors(self) -> None:
        """Warnings and infos do not invalidate the deck."""
        report = DeckValidationReport.from_issues(
            (
                DeckValidationIssue(
                    severity=DeckValidationIssueSeverity.WARNING,
                    code="W",
                    message="w",
                ),
            )
        )
        assert report.is_valid is True
