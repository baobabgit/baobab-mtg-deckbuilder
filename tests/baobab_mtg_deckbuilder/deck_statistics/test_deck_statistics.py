"""Tests for :class:`DeckStatistics`."""

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.deck_statistics.card_analytic_profile import CardAnalyticProfile
from baobab_mtg_deckbuilder.deck_statistics.deck_statistics import MANA_CURVE_CAP, DeckStatistics
from tests.baobab_mtg_deckbuilder.deck_statistics.fake_card_analytic_provider import (
    FakeCardAnalyticProvider,
)


def _deck_with_main(entries: list[DeckCardEntry]) -> Deck:
    main = DeckSection.main(entries)
    side = DeckSection.sideboard([])
    return Deck.from_sections(main, side)


class TestDeckStatistics:
    """Analytical aggregates on simple constructed-style lists."""

    def test_mana_curve_simple(self) -> None:
        """Mana curve excludes lands and buckets high costs."""
        provider = FakeCardAnalyticProvider(
            {
                "One-Drop": CardAnalyticProfile(
                    mana_value=1,
                    is_land=False,
                    color_identity=frozenset({"R"}),
                    type_categories=frozenset({"Creature"}),
                ),
                "Two-Drop": CardAnalyticProfile(
                    mana_value=2,
                    is_land=False,
                    color_identity=frozenset({"R"}),
                    type_categories=frozenset({"Creature"}),
                ),
                "Island": CardAnalyticProfile(
                    mana_value=0,
                    is_land=True,
                    color_identity=frozenset({"U"}),
                    type_categories=frozenset({"Land"}),
                ),
                "Big Spell": CardAnalyticProfile(
                    mana_value=10,
                    is_land=False,
                    color_identity=frozenset({"R"}),
                    type_categories=frozenset({"Sorcery"}),
                ),
            }
        )
        deck = _deck_with_main(
            [
                DeckCardEntry("One-Drop", 2),
                DeckCardEntry("Two-Drop", 4),
                DeckCardEntry("Island", 24),
                DeckCardEntry("Big Spell", 1),
            ]
        )
        stats = DeckStatistics.analyze(deck, provider)
        assert stats.main_spell_mana_curve == {1: 2, 2: 4, MANA_CURVE_CAP: 1}
        assert stats.main_land_quantity == 24

    def test_color_distribution_multicolor(self) -> None:
        """Each copy contributes once per color in identity."""
        provider = FakeCardAnalyticProvider(
            {
                "Monored": CardAnalyticProfile(
                    mana_value=1,
                    is_land=False,
                    color_identity=frozenset({"R"}),
                    type_categories=frozenset({"Creature"}),
                ),
                "Gold": CardAnalyticProfile(
                    mana_value=2,
                    is_land=False,
                    color_identity=frozenset({"U", "R"}),
                    type_categories=frozenset({"Creature"}),
                ),
            }
        )
        deck = _deck_with_main(
            [
                DeckCardEntry("Monored", 4),
                DeckCardEntry("Gold", 2),
            ]
        )
        stats = DeckStatistics.analyze(deck, provider)
        assert stats.main_color_quantity_by_label["R"] == 4 + 2
        assert stats.main_color_quantity_by_label["U"] == 2

    def test_type_distribution(self) -> None:
        """Types split quantities across labels."""
        provider = FakeCardAnalyticProvider(
            {
                "Bear": CardAnalyticProfile(
                    mana_value=2,
                    is_land=False,
                    color_identity=frozenset({"G"}),
                    type_categories=frozenset({"Creature"}),
                ),
                "Bolt": CardAnalyticProfile(
                    mana_value=1,
                    is_land=False,
                    color_identity=frozenset({"R"}),
                    type_categories=frozenset({"Instant"}),
                ),
            }
        )
        deck = _deck_with_main(
            [
                DeckCardEntry("Bear", 3),
                DeckCardEntry("Bolt", 1),
            ]
        )
        stats = DeckStatistics.analyze(deck, provider)
        assert stats.main_type_quantity_by_label["Creature"] == 3
        assert stats.main_type_quantity_by_label["Instant"] == 1

    def test_land_count_infers_from_types(self) -> None:
        """Land is detected via type line when ``is_land`` is unset."""
        provider = FakeCardAnalyticProvider(
            {
                "Island": CardAnalyticProfile(
                    mana_value=0,
                    is_land=None,
                    color_identity=frozenset({"U"}),
                    type_categories=frozenset({"Land", "Basic"}),
                ),
            }
        )
        deck = _deck_with_main([DeckCardEntry("Island", 24)])
        stats = DeckStatistics.analyze(deck, provider)
        assert stats.main_land_quantity == 24
        assert stats.main_spell_mana_curve == {}

    def test_quantity_by_english_name_matches_summary(self) -> None:
        """Copy counts align with :class:`DeckSummary`."""
        deck = _deck_with_main(
            [
                DeckCardEntry("A", 2),
                DeckCardEntry("B", 1),
                DeckCardEntry("A", 1),
            ]
        )
        summary = deck.summary()
        stats = DeckStatistics.analyze(deck, None)
        assert dict(stats.main_quantity_by_english_name) == dict(
            summary.main_quantity_by_english_name
        )

    def test_provider_none_marks_all_missing(self) -> None:
        """Without a provider, metadata buckets stay empty and missing is total."""
        deck = _deck_with_main([DeckCardEntry("Mystery", 15)])
        stats = DeckStatistics.analyze(deck, None)
        assert stats.main_profile_missing_quantity == 15
        assert stats.main_spell_mana_curve == {}
        assert stats.main_color_quantity_by_label == {}
        assert stats.main_type_quantity_by_label == {}
        assert stats.main_land_quantity == 0

    def test_unknown_mana_value_on_spell(self) -> None:
        """Spells without CMC increment the unknown counter."""
        provider = FakeCardAnalyticProvider(
            {
                "Walker": CardAnalyticProfile(
                    mana_value=None,
                    is_land=False,
                    color_identity=frozenset({"B"}),
                    type_categories=frozenset({"Planeswalker"}),
                ),
            }
        )
        deck = _deck_with_main([DeckCardEntry("Walker", 3)])
        stats = DeckStatistics.analyze(deck, provider)
        assert stats.main_spell_mana_value_unknown_quantity == 3
        assert stats.main_spell_mana_curve == {}

    def test_partial_provider_unknown_name(self) -> None:
        """A name without profile only increments the missing counter."""
        provider = FakeCardAnalyticProvider(
            {
                "Known": CardAnalyticProfile(
                    mana_value=1,
                    is_land=False,
                    color_identity=frozenset({"G"}),
                    type_categories=frozenset({"Creature"}),
                ),
            }
        )
        deck = _deck_with_main(
            [
                DeckCardEntry("Known", 4),
                DeckCardEntry("Unknown", 2),
            ]
        )
        stats = DeckStatistics.analyze(deck, provider)
        assert stats.main_profile_missing_quantity == 2
        assert stats.main_spell_mana_curve == {1: 4}

    def test_negative_mana_counts_as_unknown(self) -> None:
        """Negative CMC is treated like unknown for the curve."""
        provider = FakeCardAnalyticProvider(
            {
                "Broken": CardAnalyticProfile(
                    mana_value=-1,
                    is_land=False,
                    color_identity=frozenset({"B"}),
                    type_categories=frozenset({"Creature"}),
                ),
            }
        )
        deck = _deck_with_main([DeckCardEntry("Broken", 1)])
        stats = DeckStatistics.analyze(deck, provider)
        assert stats.main_spell_mana_value_unknown_quantity == 1

    def test_unknown_color_and_type_buckets(self) -> None:
        """Empty identity or type set maps to the ``?`` bucket."""
        provider = FakeCardAnalyticProvider(
            {
                "Weird": CardAnalyticProfile(
                    mana_value=2,
                    is_land=False,
                    color_identity=frozenset(),
                    type_categories=frozenset(),
                ),
            }
        )
        deck = _deck_with_main([DeckCardEntry("Weird", 2)])
        stats = DeckStatistics.analyze(deck, provider)
        assert stats.main_color_quantity_by_label["?"] == 2
        assert stats.main_type_quantity_by_label["?"] == 2

    def test_custom_color_sorted_after_wubrg(self) -> None:
        """Non-WUBRG labels are appended in deterministic order."""
        provider = FakeCardAnalyticProvider(
            {
                "Custom": CardAnalyticProfile(
                    mana_value=1,
                    is_land=False,
                    color_identity=frozenset({"Zeta"}),
                    type_categories=frozenset({"Creature"}),
                ),
            }
        )
        deck = _deck_with_main([DeckCardEntry("Custom", 1)])
        stats = DeckStatistics.analyze(deck, provider)
        assert list(stats.main_color_quantity_by_label.keys()) == ["Zeta"]
        assert stats.main_color_quantity_by_label["Zeta"] == 1
