"""Tests for :class:`DeckGenerationException`."""

import pytest

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)
from baobab_mtg_deckbuilder.exceptions.deck_generation_exception import (
    DeckGenerationException,
)


class TestDeckGenerationException:
    """Tests for generation failures."""

    def test_inherits_base(self) -> None:
        """Generation errors inherit the project base."""
        assert issubclass(DeckGenerationException, BaobabMtgDeckbuilderException)

    def test_catchable_as_base(self) -> None:
        """Callers may catch the shared project base."""
        with pytest.raises(BaobabMtgDeckbuilderException):
            raise DeckGenerationException("cannot build")
