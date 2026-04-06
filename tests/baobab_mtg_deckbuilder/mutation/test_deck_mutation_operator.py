"""Tests pour :class:`DeckMutationOperator`."""

import pytest

from baobab_mtg_deckbuilder.mutation.deck_mutation_operator import DeckMutationOperator


class TestDeckMutationOperator:
    """Contrat abstrait."""

    def test_cannot_instantiate_abstract_base(self) -> None:
        """La base abstraite n'est pas instanciable."""
        with pytest.raises(TypeError):
            DeckMutationOperator()  # type: ignore[abstract]
