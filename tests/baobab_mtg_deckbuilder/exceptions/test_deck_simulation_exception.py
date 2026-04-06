"""Tests for :class:`DeckSimulationException`."""

import pytest

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)
from baobab_mtg_deckbuilder.exceptions.deck_simulation_exception import (
    DeckSimulationException,
)


class TestDeckSimulationException:
    """Tests for simulation failures."""

    def test_inherits_base(self) -> None:
        """Simulation errors inherit the project base."""
        assert issubclass(DeckSimulationException, BaobabMtgDeckbuilderException)

    def test_catchable_as_base(self) -> None:
        """Callers may catch the shared project base."""
        with pytest.raises(BaobabMtgDeckbuilderException):
            raise DeckSimulationException("simulation unavailable")
