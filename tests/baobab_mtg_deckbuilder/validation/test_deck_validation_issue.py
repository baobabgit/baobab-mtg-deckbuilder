"""Tests for :class:`DeckValidationIssue`."""

from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)


class TestDeckValidationIssue:
    """Tests for a single validation issue."""

    def test_optional_fields(self) -> None:
        """Affected entity and suggestion may be omitted."""
        issue = DeckValidationIssue(
            severity=DeckValidationIssueSeverity.ERROR,
            code="E",
            message="msg",
        )
        assert issue.affected_entity is None
        assert issue.suggestion is None
