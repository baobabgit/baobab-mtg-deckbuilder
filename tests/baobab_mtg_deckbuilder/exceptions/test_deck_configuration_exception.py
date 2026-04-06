"""Tests for :class:`DeckConfigurationException`."""

import pytest

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)
from baobab_mtg_deckbuilder.exceptions.deck_configuration_exception import (
    DeckConfigurationException,
)


class TestDeckConfigurationException:
    """Tests for configuration failures."""

    def test_inherits_base(self) -> None:
        """Configuration errors inherit the project base."""
        assert issubclass(DeckConfigurationException, BaobabMtgDeckbuilderException)

    def test_catchable_as_base(self) -> None:
        """Callers may catch the shared project base."""
        with pytest.raises(BaobabMtgDeckbuilderException):
            raise DeckConfigurationException("bad config")
