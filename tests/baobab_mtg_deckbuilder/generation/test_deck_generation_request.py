"""Tests pour :class:`DeckGenerationRequest`."""

import pytest

from baobab_mtg_deckbuilder.exceptions.deck_generation_exception import DeckGenerationException
from baobab_mtg_deckbuilder.generation.deck_generation_request import DeckGenerationRequest
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)


class TestDeckGenerationRequest:
    """Validation des paramètres d'entrée."""

    def test_rejects_non_positive_candidate_count(self) -> None:
        """``candidate_count`` < 1 lève une erreur métier."""
        fmt = ConstructedFormatDefinition()
        pool = CardPool.from_entries((CardPoolEntry("Island", 60),), pool_kind="physical")
        with pytest.raises(DeckGenerationException, match="candidate_count"):
            DeckGenerationRequest(
                format_definition=fmt,
                pool=pool,
                random_seed=0,
                candidate_count=0,
            )

    def test_rejects_empty_pool(self) -> None:
        """Un pool sans entrées est refusé."""
        fmt = ConstructedFormatDefinition()
        pool = CardPool.from_entries((), pool_kind="physical")
        with pytest.raises(DeckGenerationException, match="aucune carte"):
            DeckGenerationRequest(
                format_definition=fmt,
                pool=pool,
                random_seed=0,
                candidate_count=1,
            )
