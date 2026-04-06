"""Tests pour :class:`DeckGenerationStrategy`."""

import random

import pytest

from baobab_mtg_deckbuilder.generation.deck_generation_strategy import DeckGenerationStrategy


class TestDeckGenerationStrategy:
    """Contrat de base."""

    def test_cannot_instantiate_abstract_base(self) -> None:
        """La classe abstraite n'est pas instanciable directement."""
        with pytest.raises(TypeError):
            DeckGenerationStrategy()  # type: ignore[abstract]

    def test_rng_for_candidate_is_stable(self) -> None:
        """Le générateur dérivé est reproductible."""
        a = DeckGenerationStrategy.rng_for_candidate(10, 2)
        b = DeckGenerationStrategy.rng_for_candidate(10, 2)
        assert isinstance(a, random.Random)
        assert isinstance(b, random.Random)
        assert a.random() == b.random()
