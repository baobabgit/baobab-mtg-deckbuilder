"""Tests for :class:`DeckValidationException`."""

import pytest

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)
from baobab_mtg_deckbuilder.exceptions.deck_validation_exception import (
    DeckValidationException,
)


class TestDeckValidationException:
    """Tests for validation failures."""

    def test_inherits_base(self) -> None:
        """Validation errors inherit the project base."""
        assert issubclass(DeckValidationException, BaobabMtgDeckbuilderException)

    def test_catchable_as_base(self) -> None:
        """Callers may catch the shared project base."""
        with pytest.raises(BaobabMtgDeckbuilderException):
            raise DeckValidationException("invalid deck")
