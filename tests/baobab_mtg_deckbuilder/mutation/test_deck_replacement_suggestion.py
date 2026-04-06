"""Tests pour :class:`DeckReplacementSuggestion`."""

import pytest

from baobab_mtg_deckbuilder.exceptions.deck_mutation_exception import DeckMutationException
from baobab_mtg_deckbuilder.mutation.deck_replacement_suggestion import DeckReplacementSuggestion


class TestDeckReplacementSuggestion:
    """Validation des paramètres de suggestion."""

    def test_rejects_non_positive_copies(self) -> None:
        """``copies`` < 1 est refusé."""
        with pytest.raises(DeckMutationException, match="copies"):
            DeckReplacementSuggestion(
                remove_english_name="A",
                add_english_name="B",
                section_identifier="main",
                copies=0,
                rationale="test",
            )
