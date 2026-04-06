"""Tests for :class:`DeckValidationIssueSeverity`."""

from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)


class TestDeckValidationIssueSeverity:
    """Tests for severity enum values."""

    def test_string_values(self) -> None:
        """StrEnum exposes stable lowercase values."""
        assert DeckValidationIssueSeverity.ERROR.value == "error"
        assert DeckValidationIssueSeverity.WARNING.value == "warning"
        assert DeckValidationIssueSeverity.INFO.value == "info"
