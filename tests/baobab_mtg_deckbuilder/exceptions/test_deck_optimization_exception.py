"""Tests for :class:`DeckOptimizationException`."""

import pytest

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)
from baobab_mtg_deckbuilder.exceptions.deck_optimization_exception import (
    DeckOptimizationException,
)


class TestDeckOptimizationException:
    """Tests for optimization failures."""

    def test_inherits_base(self) -> None:
        """Optimization errors inherit the project base."""
        assert issubclass(DeckOptimizationException, BaobabMtgDeckbuilderException)

    def test_catchable_as_base(self) -> None:
        """Callers may catch the shared project base."""
        with pytest.raises(BaobabMtgDeckbuilderException):
            raise DeckOptimizationException("optimizer failed")
