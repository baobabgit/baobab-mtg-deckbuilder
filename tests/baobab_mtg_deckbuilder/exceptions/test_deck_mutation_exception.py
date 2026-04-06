"""Tests pour :class:`DeckMutationException`."""

import pytest

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)
from baobab_mtg_deckbuilder.exceptions.deck_mutation_exception import DeckMutationException


class TestDeckMutationException:
    """Hiérarchie d'erreurs mutations."""

    def test_inherits_base(self) -> None:
        """Les erreurs de mutation héritent de la base projet."""
        assert issubclass(DeckMutationException, BaobabMtgDeckbuilderException)

    def test_catchable_as_base(self) -> None:
        """Les appelants peuvent intercepter la base commune."""
        with pytest.raises(BaobabMtgDeckbuilderException):
            raise DeckMutationException("impossible")
