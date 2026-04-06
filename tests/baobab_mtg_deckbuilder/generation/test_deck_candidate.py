"""Tests pour :class:`DeckCandidate`."""

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.generation.deck_candidate import DeckCandidate
from baobab_mtg_deckbuilder.validation.deck_validation_issue import DeckValidationIssue
from baobab_mtg_deckbuilder.validation.deck_validation_issue_severity import (
    DeckValidationIssueSeverity,
)
from baobab_mtg_deckbuilder.validation.deck_validation_report import DeckValidationReport


class TestDeckCandidate:
    """Propriétés dérivées du candidat."""

    def test_is_valid_follows_report(self) -> None:
        """``is_valid`` reflète l'absence d'erreurs dans le rapport."""
        deck = Deck.from_sections(
            DeckSection.main((DeckCardEntry("Island", 1),)),
            DeckSection.sideboard(()),
        )
        ok = DeckValidationReport.from_issues(())
        bad = DeckValidationReport.from_issues(
            (
                DeckValidationIssue(
                    severity=DeckValidationIssueSeverity.ERROR,
                    code="X",
                    message="m",
                    affected_entity=None,
                    suggestion=None,
                ),
            )
        )
        assert DeckCandidate(0, deck, ok).is_valid is True
        assert DeckCandidate(0, deck, bad).is_valid is False
