"""Tests du builder de main deck."""

import random

import pytest

from baobab_mtg_deckbuilder.exceptions.deck_generation_exception import DeckGenerationException
from baobab_mtg_deckbuilder.generation.maindeck_from_pool_builder import (
    build_maindeck_candidate,
    main_minimum_for_format,
)
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)
from baobab_mtg_deckbuilder.validation.limited_format_definition import LimitedFormatDefinition
from tests.baobab_mtg_deckbuilder.generation.unsupported_format_definition import (
    UnsupportedFormatDefinitionForTests,
)


class TestMaindeckFromPoolBuilder:
    """Construction depuis un pool typé."""

    def test_main_minimum_for_constructed_and_limited(self) -> None:
        """Les minimums annoncés correspondent aux formats MVP."""
        assert main_minimum_for_format(ConstructedFormatDefinition()) == 60
        assert main_minimum_for_format(LimitedFormatDefinition()) == 40

    def test_unsupported_format_raises(self) -> None:
        """Un format hors périmètre lève :class:`DeckGenerationException`."""
        fmt = UnsupportedFormatDefinitionForTests()
        with pytest.raises(DeckGenerationException, match="non pris en charge"):
            main_minimum_for_format(fmt)

    def test_build_rejects_unsupported_format(self) -> None:
        """Le builder refuse les formats inconnus."""
        fmt = UnsupportedFormatDefinitionForTests()
        pool = CardPool.from_entries((CardPoolEntry("Island", 60),), pool_kind="physical")
        with pytest.raises(DeckGenerationException, match="non pris en charge"):
            build_maindeck_candidate(
                pool,
                fmt,
                rng=random.Random(0),
                shuffle_nonbasics=False,
                shuffle_basics=False,
                nonbasic_priority="alphabetical",
                candidate_index=0,
                apply_list_rotation=False,
            )

    def test_insufficient_pool_raises(self) -> None:
        """Impossible d'atteindre la taille minimale du main."""
        fmt = ConstructedFormatDefinition()
        pool = CardPool.from_entries((CardPoolEntry("Island", 30),), pool_kind="physical")
        with pytest.raises(DeckGenerationException, match="insuffisant"):
            build_maindeck_candidate(
                pool,
                fmt,
                rng=random.Random(0),
                shuffle_nonbasics=False,
                shuffle_basics=False,
                nonbasic_priority="alphabetical",
                candidate_index=0,
                apply_list_rotation=False,
            )

    def test_constructed_valid_main_from_nonbasics(self) -> None:
        """60 cartes hors bases respectent la règle des 4 exemplaires."""
        fmt = ConstructedFormatDefinition()
        entries = tuple(CardPoolEntry(f"Spell {i:02d}", 4) for i in range(15))
        pool = CardPool.from_entries(entries, pool_kind="physical")
        deck = build_maindeck_candidate(
            pool,
            fmt,
            rng=random.Random(0),
            shuffle_nonbasics=False,
            shuffle_basics=False,
            nonbasic_priority="alphabetical",
            candidate_index=0,
            apply_list_rotation=False,
        )
        report = fmt.validate(deck)
        assert deck.main_total_quantity == 60
        assert report.is_valid is True

    def test_theoretical_none_bounded_internally(self) -> None:
        """Les quantités ``None`` sont bornées pour permettre la construction."""
        fmt = LimitedFormatDefinition()
        pool = CardPool.from_entries((CardPoolEntry("Any", None),), pool_kind="theoretical")
        deck = build_maindeck_candidate(
            pool,
            fmt,
            rng=random.Random(1),
            shuffle_nonbasics=False,
            shuffle_basics=False,
            nonbasic_priority="alphabetical",
            candidate_index=0,
            apply_list_rotation=False,
        )
        assert deck.main_total_quantity == 40
        assert fmt.validate(deck).is_valid is True

    def test_rotation_changes_multiset_when_pool_is_tight(self) -> None:
        """La rotation gloutonne modifie la répartition quand le pool est serré."""
        fmt = ConstructedFormatDefinition()
        entries = tuple(CardPoolEntry(f"Card {chr(65 + i)}", 3) for i in range(25))
        pool = CardPool.from_entries(entries, pool_kind="physical")
        first = build_maindeck_candidate(
            pool,
            fmt,
            rng=random.Random(0),
            shuffle_nonbasics=False,
            shuffle_basics=False,
            nonbasic_priority="alphabetical",
            candidate_index=0,
            apply_list_rotation=True,
        )
        second = build_maindeck_candidate(
            pool,
            fmt,
            rng=random.Random(0),
            shuffle_nonbasics=False,
            shuffle_basics=False,
            nonbasic_priority="alphabetical",
            candidate_index=1,
            apply_list_rotation=True,
        )
        assert first.list_view().main_entries != second.list_view().main_entries
