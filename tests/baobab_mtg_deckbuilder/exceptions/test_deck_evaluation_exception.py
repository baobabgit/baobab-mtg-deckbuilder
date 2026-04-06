"""Tests for :class:`DeckEvaluationException`."""

from baobab_mtg_deckbuilder.exceptions.baobab_mtg_deckbuilder_exception import (
    BaobabMtgDeckbuilderException,
)
from baobab_mtg_deckbuilder.exceptions.deck_evaluation_exception import (
    DeckEvaluationException,
)


class TestDeckEvaluationException:
    """Hierarchy placement."""

    def test_is_baobab_subclass(self) -> None:
        """Deck evaluation errors are project-scoped."""
        assert issubclass(DeckEvaluationException, BaobabMtgDeckbuilderException)
