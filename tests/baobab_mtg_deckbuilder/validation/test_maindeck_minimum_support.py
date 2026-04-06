"""Tests for ``maindeck_minimum_support``."""

from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)
from baobab_mtg_deckbuilder.validation.maindeck_minimum_support import (
    issues_when_main_below_minimum,
)


class TestMaindeckMinimumSupport:
    """Tests for shared main-size helper."""

    def test_empty_when_at_or_above_minimum(self) -> None:
        """No issue when threshold met."""
        assert (
            issues_when_main_below_minimum(
                60,
                60,
                error_code="X",
                message="m",
                suggestion="s",
            )
            == ()
        )

    def test_error_when_below(self) -> None:
        """Returns one error below threshold."""
        issues = issues_when_main_below_minimum(
            59,
            60,
            error_code="TOO_SMALL",
            message="too small",
            suggestion="add cards",
        )
        assert len(issues) == 1
        assert issues[0].severity == DeckValidationIssueSeverity.ERROR
        assert issues[0].code == "TOO_SMALL"
