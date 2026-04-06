"""Tests d'intégration des stratégies de génération."""

from baobab_mtg_deckbuilder.generation.constrained_generation_strategy import (
    ConstrainedGenerationStrategy,
)
from baobab_mtg_deckbuilder.generation.deck_generation_request import DeckGenerationRequest
from baobab_mtg_deckbuilder.generation.greedy_generation_strategy import GreedyGenerationStrategy
from baobab_mtg_deckbuilder.generation.hybrid_generation_strategy import HybridGenerationStrategy
from baobab_mtg_deckbuilder.generation.random_seeded_generation_strategy import (
    RandomSeededGenerationStrategy,
)
from baobab_mtg_deckbuilder.pool.card_pool import CardPool
from baobab_mtg_deckbuilder.pool.card_pool_entry import CardPoolEntry
from baobab_mtg_deckbuilder.validation.constructed_format_definition import (
    ConstructedFormatDefinition,
)
from baobab_mtg_deckbuilder.validation.limited_format_definition import LimitedFormatDefinition


def _constructed_pool_sixty_nonbasics() -> CardPool:
    entries = tuple(CardPoolEntry(f"Spell {i:02d}", 4) for i in range(15))
    return CardPool.from_entries(entries, pool_kind="physical")


def _constructed_pool_shuffle_sensitive() -> CardPool:
    """75 cartes non-base (25 noms × 3) : seuls 20 noms peuvent entrer au main (60 cartes)."""
    entries = tuple(CardPoolEntry(f"Spell {i:02d}", 3) for i in range(25))
    return CardPool.from_entries(entries, pool_kind="physical")


class TestGenerationStrategies:
    """Reproductibilité, validité et divergence entre stratégies."""

    def test_greedy_produces_multiple_valid_constructed_decks(self) -> None:
        """La stratégie gloutonne remplit un construit légal lorsque le pool le permet."""
        fmt = ConstructedFormatDefinition()
        pool = _constructed_pool_sixty_nonbasics()
        request = DeckGenerationRequest(
            format_definition=fmt,
            pool=pool,
            random_seed=7,
            candidate_count=4,
        )
        result = GreedyGenerationStrategy().generate(request)
        assert result.strategy_key == "greedy"
        assert len(result.candidates) == 4
        for candidate in result.candidates:
            assert candidate.is_valid is True
            assert candidate.deck.main_total_quantity == 60
            assert candidate.deck.sideboard_total_quantity == 0

    def test_random_seeded_is_deterministic(self) -> None:
        """Même graine ⇒ mêmes decks (tous indices confondus)."""
        fmt = ConstructedFormatDefinition()
        pool = _constructed_pool_sixty_nonbasics()
        req = DeckGenerationRequest(
            format_definition=fmt,
            pool=pool,
            random_seed=12345,
            candidate_count=3,
        )
        strategy = RandomSeededGenerationStrategy()
        first = strategy.generate(req)
        second = strategy.generate(req)
        assert [c.deck.list_view().main_entries for c in first.candidates] == [
            c.deck.list_view().main_entries for c in second.candidates
        ]

    def test_random_changes_with_seed(self) -> None:
        """Deux graines distinctes produisent des multisets différents si le pool est serré."""
        fmt = ConstructedFormatDefinition()
        pool = _constructed_pool_shuffle_sensitive()
        a = RandomSeededGenerationStrategy().generate(
            DeckGenerationRequest(fmt, pool, random_seed=1, candidate_count=1)
        )
        b = RandomSeededGenerationStrategy().generate(
            DeckGenerationRequest(fmt, pool, random_seed=999_999, candidate_count=1)
        )
        assert (
            a.candidates[0].deck.list_view().main_entries
            != b.candidates[0].deck.list_view().main_entries
        )

    def test_strategies_differ_on_first_candidate(self) -> None:
        """Comparaison basique : sous-ensemble glouton vs sous-ensemble aléatoire (pool serré)."""
        fmt = ConstructedFormatDefinition()
        pool = _constructed_pool_shuffle_sensitive()
        base = DeckGenerationRequest(fmt, pool, random_seed=42, candidate_count=1)
        greedy = (
            GreedyGenerationStrategy().generate(base).candidates[0].deck.list_view().main_entries
        )
        rnd = (
            RandomSeededGenerationStrategy()
            .generate(base)
            .candidates[0]
            .deck.list_view()
            .main_entries
        )
        assert greedy != rnd

    def test_limited_format_respected(self) -> None:
        """Le format limité MVP est satisfait avec un pool suffisant."""
        fmt = LimitedFormatDefinition()
        entries = tuple(CardPoolEntry(f"Limited {i:02d}", 2) for i in range(30))
        pool = CardPool.from_entries(entries, pool_kind="physical")
        request = DeckGenerationRequest(
            format_definition=fmt,
            pool=pool,
            random_seed=0,
            candidate_count=2,
        )
        result = ConstrainedGenerationStrategy().generate(request)
        for candidate in result.candidates:
            assert candidate.deck.main_total_quantity == 40
            assert candidate.is_valid is True

    def test_hybrid_alternates_modes(self) -> None:
        """Indices pairs = glouton, impairs = aléatoire semé ; tous valides si le pool le permet."""
        fmt = ConstructedFormatDefinition()
        pool = _constructed_pool_shuffle_sensitive()
        request = DeckGenerationRequest(
            format_definition=fmt,
            pool=pool,
            random_seed=11,
            candidate_count=4,
        )
        result = HybridGenerationStrategy().generate(request)
        assert all(c.is_valid for c in result.candidates)
        even_main = result.candidates[0].deck.list_view().main_entries
        odd_main = result.candidates[1].deck.list_view().main_entries
        assert even_main != odd_main
