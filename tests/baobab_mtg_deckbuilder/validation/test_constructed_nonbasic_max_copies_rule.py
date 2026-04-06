"""Tests for :class:`ConstructedNonbasicMaxCopiesRule`."""

from baobab_mtg_deckbuilder.deck.deck import Deck
from baobab_mtg_deckbuilder.deck.deck_card_entry import DeckCardEntry
from baobab_mtg_deckbuilder.deck.deck_section import DeckSection
from baobab_mtg_deckbuilder.validation.basic_land_oracle_names import (
    DEFAULT_BASIC_LAND_ORACLE_NAMES,
)
from baobab_mtg_deckbuilder.validation.constructed_nonbasic_max_copies_rule import (
    ConstructedNonbasicMaxCopiesRule,
)


class TestConstructedNonbasicMaxCopiesRule:
    """Unit tests for the 4-copy rule."""

    def test_rule_id_stable(self) -> None:
        """Rule id is documented and stable."""
        rule = ConstructedNonbasicMaxCopiesRule(DEFAULT_BASIC_LAND_ORACLE_NAMES, 4)
        assert rule.rule_id == "constructed.nonbasic_max_copies"

    def test_allows_basic_lands(self) -> None:
        """Ten Forest is legal."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Forest", 10)]),
            DeckSection.sideboard([]),
        )
        rule = ConstructedNonbasicMaxCopiesRule(DEFAULT_BASIC_LAND_ORACLE_NAMES, 4)
        assert rule.evaluate(deck) == ()

    def test_flags_excess_nonbasic(self) -> None:
        """Five Shocks illegal."""
        deck = Deck.from_sections(
            DeckSection.main([DeckCardEntry("Shock", 5)]),
            DeckSection.sideboard([]),
        )
        rule = ConstructedNonbasicMaxCopiesRule(DEFAULT_BASIC_LAND_ORACLE_NAMES, 4)
        issues = rule.evaluate(deck)
        assert len(issues) == 1
        assert issues[0].affected_entity == "Shock"
